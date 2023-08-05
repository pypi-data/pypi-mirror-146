import pdme.inputs
import pdme.model
import pdme.measurement.input_types
import pdme.measurement.oscillating_dipole
import pdme.util.fast_v_calc
import pdme.util.fast_nonlocal_spectrum
from typing import Sequence, Tuple, List
import datetime
import csv
import multiprocessing
import logging
import numpy


# TODO: remove hardcode
CHUNKSIZE = 50

# TODO: It's garbage to have this here duplicated from pdme.
DotInput = Tuple[numpy.typing.ArrayLike, float]


_logger = logging.getLogger(__name__)


def get_a_result(input) -> int:
	discretisation, dot_inputs, lows, highs, monte_carlo_count, max_frequency = input
	sample_dipoles = discretisation.get_model().get_n_single_dipoles(monte_carlo_count, max_frequency)
	vals = pdme.util.fast_v_calc.fast_vs_for_dipoles(dot_inputs, sample_dipoles)
	return numpy.count_nonzero(pdme.util.fast_v_calc.between(vals, lows, highs))


def get_a_result_using_pairs(input) -> int:
	discretisation, dot_inputs, pair_inputs, local_lows, local_highs, nonlocal_lows, nonlocal_highs, monte_carlo_count, max_frequency = input
	sample_dipoles = discretisation.get_model().get_n_single_dipoles(monte_carlo_count, max_frequency)
	local_vals = pdme.util.fast_v_calc.fast_vs_for_dipoles(dot_inputs, sample_dipoles)
	local_matches = pdme.util.fast_v_calc.between(local_vals, local_lows, local_highs)
	nonlocal_vals = pdme.util.fast_nonlocal_spectrum.fast_s_nonlocal(pair_inputs, sample_dipoles)
	nonlocal_matches = pdme.util.fast_v_calc.between(nonlocal_vals, nonlocal_lows, nonlocal_highs)
	combined_matches = numpy.logical_and(local_matches, nonlocal_matches)
	return numpy.count_nonzero(combined_matches)


class AltBayesRun():
	'''
	A single Bayes run for a given set of dots.

	Parameters
	----------
	dot_inputs : Sequence[DotInput]
		The dot inputs for this bayes run.
	discretisations_with_names : Sequence[Tuple(str, pdme.model.Model)]
		The models to evaluate.
	actual_model_discretisation : pdme.model.Discretisation
		The discretisation for the model which is actually correct.
	filename_slug : str
		The filename slug to include.
	run_count: int
		The number of runs to do.
	'''
	def __init__(self, dot_positions: Sequence[numpy.typing.ArrayLike], frequency_range: Sequence[float], discretisations_with_names: Sequence[Tuple[str, pdme.model.Discretisation]], actual_model: pdme.model.Model, filename_slug: str, run_count: int = 100, low_error: float = 0.9, high_error: float = 1.1, pairs_high_error=None, pairs_low_error=None, monte_carlo_count: int = 10000, monte_carlo_cycles: int = 10, target_success: int = 100, max_monte_carlo_cycles_steps: int = 10, max_frequency: float = 20, end_threshold: float = None, chunksize: int = CHUNKSIZE, use_pairs: bool = False) -> None:
		self.dot_inputs = pdme.inputs.inputs_with_frequency_range(dot_positions, frequency_range)
		self.dot_inputs_array = pdme.measurement.input_types.dot_inputs_to_array(self.dot_inputs)

		self.use_pairs = use_pairs

		self.dot_pair_inputs = pdme.inputs.input_pairs_with_frequency_range(dot_positions, frequency_range)
		self.dot_pair_inputs_array = pdme.measurement.input_types.dot_pair_inputs_to_array(self.dot_pair_inputs)

		self.discretisations = [disc for (_, disc) in discretisations_with_names]
		self.model_names = [name for (name, _) in discretisations_with_names]
		self.actual_model = actual_model
		self.model_count = len(self.discretisations)
		self.monte_carlo_count = monte_carlo_count
		self.monte_carlo_cycles = monte_carlo_cycles
		self.target_success = target_success
		self.max_monte_carlo_cycles_steps = max_monte_carlo_cycles_steps
		self.run_count = run_count
		self.low_error = low_error
		self.high_error = high_error
		if pairs_low_error is None:
			self.pairs_low_error = self.low_error
		else:
			self.pairs_low_error = pairs_low_error
		if pairs_high_error is None:
			self.pairs_high_error = self.high_error
		else:
			self.pairs_high_error = pairs_high_error
		self.csv_fields = ["dipole_moment", "dipole_location", "dipole_frequency"]
		self.compensate_zeros = True
		self.chunksize = chunksize
		for name in self.model_names:
			self.csv_fields.extend([f"{name}_success", f"{name}_count", f"{name}_prob"])

		self.probabilities = [1 / self.model_count] * self.model_count

		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
		if self.use_pairs:
			self.filename = f"{timestamp}-{filename_slug}.altbayes.pairs.csv"
		else:
			self.filename = f"{timestamp}-{filename_slug}.altbayes.csv"
		self.max_frequency = max_frequency

		if end_threshold is not None:
			if 0 < end_threshold < 1:
				self.end_threshold: float = end_threshold
				self.use_end_threshold = True
				_logger.info(f"Will abort early, at {self.end_threshold}.")
			else:
				raise ValueError(f"end_threshold should be between 0 and 1, but is actually {end_threshold}")

	def go(self) -> None:
		with open(self.filename, "a", newline="") as outfile:
			writer = csv.DictWriter(outfile, fieldnames=self.csv_fields, dialect="unix")
			writer.writeheader()

		for run in range(1, self.run_count + 1):

			rng = numpy.random.default_rng()
			frequency = rng.uniform(1, self.max_frequency)

			# Generate the actual dipoles
			actual_dipoles = self.actual_model.get_dipoles(frequency)

			dots = actual_dipoles.get_percent_range_dot_measurements(self.dot_inputs, self.low_error, self.high_error)
			lows, highs = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(dots)

			pair_lows, pair_highs = (None, None)
			if self.use_pairs:
				pair_measurements = actual_dipoles.get_percent_range_dot_pair_measurements(self.dot_pair_inputs, self.pairs_low_error, self.pairs_high_error)
				pair_lows, pair_highs = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(pair_measurements)

			_logger.info(f"Going to work on dipole at {actual_dipoles.dipoles}")

			results = []
			_logger.debug("Going to iterate over discretisations now")
			for disc_count, discretisation in enumerate(self.discretisations):
				_logger.debug(f"Doing discretisation #{disc_count}")
				with multiprocessing.Pool(multiprocessing.cpu_count() - 1 or 1) as pool:
					cycle_count = 0
					cycle_success = 0
					cycles = 0
					while (cycles < self.max_monte_carlo_cycles_steps) and (cycle_success <= self.target_success):
						_logger.debug(f"Starting cycle {cycles}")
						cycles += 1
						current_success = 0
						cycle_count += self.monte_carlo_count * self.monte_carlo_cycles
						if self.use_pairs:
							current_success = sum(
								pool.imap_unordered(get_a_result_using_pairs, [(discretisation, self.dot_inputs_array, self.dot_pair_inputs_array, lows, highs, pair_lows, pair_highs, self.monte_carlo_count, self.max_frequency)] * self.monte_carlo_cycles, self.chunksize)
							)
						else:
							current_success = sum(
								pool.imap_unordered(get_a_result, [(discretisation, self.dot_inputs_array, lows, highs, self.monte_carlo_count, self.max_frequency)] * self.monte_carlo_cycles, self.chunksize)
							)

						cycle_success += current_success
					results.append((cycle_count, cycle_success))

			_logger.debug("Done, constructing output now")
			row = {
				"dipole_moment": actual_dipoles.dipoles[0].p,
				"dipole_location": actual_dipoles.dipoles[0].s,
				"dipole_frequency": actual_dipoles.dipoles[0].w
			}
			successes: List[float] = []
			counts: List[int] = []
			for model_index, (name, (count, result)) in enumerate(zip(self.model_names, results)):

				row[f"{name}_success"] = result
				row[f"{name}_count"] = count
				successes.append(max(result, 0.5))
				counts.append(count)

			success_weight = sum([(succ / count) * prob for succ, count, prob in zip(successes, counts, self.probabilities)])
			new_probabilities = [(succ / count) * old_prob / success_weight for succ, count, old_prob in zip(successes, counts, self.probabilities)]
			self.probabilities = new_probabilities
			for name, probability in zip(self.model_names, self.probabilities):
				row[f"{name}_prob"] = probability
			_logger.info(row)

			with open(self.filename, "a", newline="") as outfile:
				writer = csv.DictWriter(outfile, fieldnames=self.csv_fields, dialect="unix")
				writer.writerow(row)

			if self.use_end_threshold:
				max_prob = max(self.probabilities)
				if max_prob > self.end_threshold:
					_logger.info(f"Aborting early, because {max_prob} is greater than {self.end_threshold}")
					break
