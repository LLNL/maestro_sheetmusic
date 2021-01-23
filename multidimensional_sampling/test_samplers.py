"""
Sampler Tests

Tests for codepy/maestro integration:

#. ListSampler,
#. ColumnListSampler,
#. CrossProductSampler,
#. RandomSampler,
#. BestCandidateSampler,
#. CsvSampler,
#. CustomSampler
"""
# @TODO: read required output from yaml file, run grep, fail if appropriate, loop through files

import os
import shutil
import tempfile
import unittest
import time
from contextlib import suppress

import pytest
import yaml


class TestScisampleMaestroPgen(unittest.TestCase):
    """
    Scenario: Test all 'sample_*.yaml' files
    """
    def setUp(self):
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        pass
        #shutil.rmtree(self.tmp_dir, ignore_errors=True)

    # @TODO: For these tests, we should test that all runs have finished.
    # @TODO: Currently, `check_status` succeeds if at least one run is finished.
    def check_status(self, study_path_maestro):
        """
        Check if the study has run.
        """
        if not os.path.exists(study_path_maestro):
            return False

        output = os.popen(f"maestro status {study_path_maestro}").read()
        for line in output.splitlines()[::-1]:
            state = line.split()[2]
            if state == '-'*len(state):
                return True
            if state == 'FINISHED':
                continue
            if state == 'FAILED':
                raise ValueError("Study failed")
            return False

    def test_setup(self):
        self.assertTrue(os.path.isdir(self.tmp_dir))

    def test_samplers(self):
        """
        Given a set of 'sample_*.yaml' files in the current directory,
        And I run each one through maestro,
        Then I should get the expected output defined in the 'sample_*.yaml' files
        """
        sample_files = ['sample_list.yaml']
        output_dir = 'output'
        studies_directory = os.path.join(self.tmp_dir, output_dir)

        for sample_file in sample_files:
            shutil.copyfile(
                os.path.join(self.script_path, sample_file),
                os.path.join(self.tmp_dir, sample_file))
            os.chdir(self.tmp_dir)

            execute_string = (
                f"maestro run -y --pgen `which pgen_scisample.py` "
                f" {sample_file}")
            output = os.popen(execute_string).read()
            print(f"output:\n{output}")

            dirs = os.listdir(studies_directory)
            study_path = os.path.join(studies_directory, dirs[0])

            for i in range(60):
                time.sleep(3)
                if self.check_status(study_path):
                    break
            else:
                raise ValueError("Study did not finish within 3 minutes")

            output_files_pattern = os.path.join(
                self.tmp_dir,'output','*','sample','*','out.txt')
            execute_string = (f"ls {output_files_pattern}")
            print(f"execute_string: {execute_string}")
            output = os.popen(execute_string).read()
            print(f"output:\n{output}") 
            pass
        self.assertEqual(0, 1)





#         yaml_text = """
#             foo: bar
#             #constants:
#             #    X1: 20
#             #parameters:
#             #   X2: [5, 10]
#             #   X3: [5, 10]
#             """
#         with self.assertRaises(SamplingError) as context:
#             new_sampler_from_yaml(yaml_text)
#         self.assertTrue(
#             "No type entry in sampler data"
#             in str(context.exception))

#     def test_invalid_type_exception(self):
#         """
#         Given an invalid sampler type,
#         And I request a new sampler
#         Then I should get a SamplerException
#         """
#         yaml_text = """
#             type: foobar
#             #constants:
#             #    X1: 20
#             #parameters:
#             #   X2: [5, 10]
#             #   X3: [5, 10]
#             """
#         with self.assertRaises(SamplingError) as context:
#             new_sampler_from_yaml(yaml_text)
#         self.assertTrue(
#             "not a recognized sampler type"
#             in str(context.exception))

#     def test_missing_data_exception(self):
#         """
#         Given no constants or parameters
#         And I request a new sampler
#         Then I should get a SamplerException
#         """
#         yaml_text = """
#             type: list
#             #constants:
#             #    X1: 20
#             #parameters:
#             #   X2: [5, 10]
#             #   X3: [5, 10]
#             """
#         with self.assertRaises(SamplingError) as context:
#             new_sampler_from_yaml(yaml_text)
#         self.assertTrue(
#             "Either constants or parameters must be included"
#             in str(context.exception))

#     def test_duplicate_data_exception(self):
#         """
#         Given a variable in both constants and parameters
#         And I request a new sampler
#         Then I should get a SamplerException
#         """
#         # @TODO: We can not detect if parameters are defined twice.
#         # @TODO: Fixing this requires a rewrite of read_yaml.
#         yaml_text = """
#             type: list
#             constants:
#                 X2: 20
#             parameters:
#                 X2: [5, 10]
#                 X2: [5, 10]
#                 X3: [5, 10]
#                 X3: [5, 10]
#              """
#         with self.assertRaises(SamplingError) as context:
#             new_sampler_from_yaml(yaml_text)
#         self.assertTrue(
#             "The following constants or parameters are defined more than once"
#             in str(context.exception))


# class TestScisampleUniversal(unittest.TestCase):
#     """
#     Scenario: Testing behavior valid for multiple samplers
#     """
#     def test_constants_only(self):
#         """
#         Given only constants
#         And I request a new sampler
#         Then I should get a sampler with one sample
#         With appropriate values
#         """
#         yaml_text = """
#             type: list
#             constants:
#                 X1: 20
#                 X2: 30
#             #parameters:
#             #    X2: [5, 10]
#             #    X3: [5, 10]
#             """
#         sampler = new_sampler_from_yaml(yaml_text)
#         samples = sampler.get_samples()

#         self.assertEqual(len(samples), 1)
#         for sample in samples:
#             self.assertEqual(sample['X1'], 20)
#             self.assertEqual(sample['X2'], 30)

#     def test_parameters_only(self):
#         """
#         Given only parameters
#         And I request a new sampler
#         Then I should get appropriate values
#         """
#         yaml_text = """
#             type: list
#             #constants:
#             #    X1: 20
#             parameters:
#                 X2: [5, 10]
#                 X3: [5, 10]
#             """
#         sampler = new_sampler_from_yaml(yaml_text)
#         samples = sampler.get_samples()

#         self.assertEqual(len(samples), 2)

#         self.assertEqual(samples[0]['X2'], 5)
#         self.assertEqual(samples[0]['X3'], 5)
#         self.assertEqual(samples[1]['X2'], 10)
#         self.assertEqual(samples[1]['X3'], 10)


# class TestScisampleList(unittest.TestCase):
#     """
#     Scenario: normal and abnormal tests for ListSampler
#     """

#     def test_normal(self):
#         """
#         Given a list specification
#         And I request a new sampler
#         Then I should get a ListSampler
#         With appropriate values
#         """
#         yaml_text = """
#             type: list
#             constants:
#                 X1: 20
#             parameters:
#                 X2: [5, 10]
#                 X3: [5, 10]
#                 X4: [5, 10]
#             """
#         sampler = new_sampler_from_yaml(yaml_text)
#         self.assertTrue(isinstance(sampler, ListSampler))

#         samples = sampler.get_samples()

#         self.assertEqual(len(samples), 2)
#         for sample in samples:
#             self.assertEqual(sample['X1'], 20)
#         self.assertEqual(samples[0]['X2'], 5)
#         self.assertEqual(samples[0]['X3'], 5)
#         self.assertEqual(samples[0]['X4'], 5)
#         self.assertEqual(samples[1]['X2'], 10)
#         self.assertEqual(samples[1]['X3'], 10)
#         self.assertEqual(samples[1]['X4'], 10)
#         sampler
#         self.assertEqual(samples, 
#             [{'X1': 20, 'X2': 5, 'X3': 5, 'X4': 5}, 
#              {'X1': 20, 'X2': 10, 'X3': 10, 'X4': 10}])
#         self.assertEqual(sampler.parameter_block, 
#             {'X1': {'values': [20, 20], 'label': 'X1.%%'}, 
#              'X2': {'values': [5, 10], 'label': 'X2.%%'}, 
#              'X3': {'values': [5, 10], 'label': 'X3.%%'}, 
#              'X4': {'values': [5, 10], 'label': 'X4.%%'}})

#     def test_error(self):
#         """
#         Given an invalid list specification
#         And I request a new sampler
#         Then I should get a SamplerException
#         """
#         yaml_text = """
#             type: list
#             constants:
#                 X1: 20
#             parameters:
#                 X2: [5, 10, 20]
#                 X3: [5, 10]
#                 X4: [5, 10]
#             """
#         with self.assertRaises(SamplingError) as context:
#             new_sampler_from_yaml(yaml_text)
#         self.assertTrue(
#             "All parameters must have the same number of values"
#             in str(context.exception))


# class TestScisampleCrossProduct(unittest.TestCase):
#     """
#     Scenario: normal tests for CrossProductSampler
#     """
#     def test_normal(self):
#         """
#         Given a cross_product specification
#         And I request a new sampler
#         Then I should get a CrossProductSampler
#         With appropriate values
#         """
#         yaml_text = """
#             # sampler:
#                 type: cross_product
#                 constants:
#                     X1: 20
#                 parameters:
#                     X2: [5, 10]
#                     X3: [5, 10]
#             """
#         sampler = new_sampler_from_yaml(yaml_text)
#         self.assertTrue(isinstance(sampler, CrossProductSampler))

#         samples = sampler.get_samples()

#         self.assertEqual(sampler.parameters, ["X1", "X2", "X3"])
#         self.assertEqual(len(samples), 4)

#         for sample in samples:
#             self.assertEqual(sample['X1'], 20)
#         self.assertEqual(samples[0]['X2'], 5)
#         self.assertEqual(samples[0]['X3'], 5)
#         self.assertEqual(samples[1]['X2'], 5)
#         self.assertEqual(samples[1]['X3'], 10)
#         self.assertEqual(samples[2]['X2'], 10)
#         self.assertEqual(samples[2]['X3'], 5)
#         self.assertEqual(samples[3]['X2'], 10)
#         self.assertEqual(samples[3]['X3'], 10)


# class TestScisampleColumnList(unittest.TestCase):
#     """
#     Scenario: normal and abnormal tests for ColumnListSampler
#     """
#     def test_normal(self):
#         """
#         Given a column_list specification
#         And I request a new sampler
#         Then I should get a ColumnListSampler
#         With appropriate values
#         """
#         yaml_text = """
#             type: column_list
#             constants:
#                 X1: 20
#             parameters: |
#                 X2     X3     X4
#                 5      5      5
#                 10     10     10
#             """
#         sampler = new_sampler_from_yaml(yaml_text)
#         self.assertTrue(isinstance(sampler, ColumnListSampler))

#         samples = sampler.get_samples()

#         self.assertEqual(len(samples), 2)
#         for sample in samples:
#             self.assertEqual(sample['X1'], 20)
#         self.assertEqual(samples[0]['X2'], '5')
#         self.assertEqual(samples[0]['X3'], '5')
#         self.assertEqual(samples[0]['X4'], '5')
#         self.assertEqual(samples[1]['X2'], '10')
#         self.assertEqual(samples[1]['X3'], '10')
#         self.assertEqual(samples[1]['X4'], '10')

#     def test_error(self):
#         """
#         Given an invalid column_list specification
#         And I request a new sampler
#         Then I should get a SamplerException
#         """
#         yaml_text = """
#             type: column_list
#             constants:
#                 X1: 20
#             parameters: |
#                 X2     X3     X4
#                 5      5      5
#                 10     10     10
#                 20
#             """
#         with self.assertRaises(SamplingError) as context:
#             new_sampler_from_yaml(yaml_text)
#         self.assertTrue(
#             "All rows must have the same number of values"
#             in str(context.exception))


# class TestScisampleRandomSampler(unittest.TestCase):
#     """
#     Scenario: normal and abnormal tests for RandomSampler
#     """
#     def test_normal(self):
#         """
#         Given a random specification
#         And I request a new sampler
#         Then I should get a RandomSampler
#         With appropriate values
#         """
#         yaml_text = """
#             type: random
#             num_samples: 5
#             #previous_samples: samples.csv # optional
#             constants:
#                 X1: 20
#             parameters:
#                 X2:
#                     min: 5
#                     max: 10
#                 X3:
#                     min: 5
#                     max: 10
#             """
#         sampler = new_sampler_from_yaml(yaml_text)
#         self.assertTrue(isinstance(sampler, RandomSampler))

#         samples = sampler.get_samples()

#         self.assertEqual(len(samples), 5)
#         for sample in samples:
#             self.assertEqual(sample['X1'], 20)
#             self.assertTrue(sample['X2'] > 5)
#             self.assertTrue(sample['X3'] > 5)
#             self.assertTrue(sample['X2'] < 10)
#             self.assertTrue(sample['X3'] < 10)

#     def test_normal2(self):
#         """
#         Given a random specification
#         And I request a new sampler
#         Then I should get a RandomSampler
#         With appropriate values
#         """
#         yaml_text = """
#             type: random
#             num_samples: 5
#             #previous_samples: samples.csv # optional
#             constants:
#                 X1: 0.5
#             parameters:
#                 X2:
#                     min: 0.2
#                     max: 0.8
#                 X3:
#                     min: 0.2
#                     max: 0.8
#             """
#         sampler = new_sampler_from_yaml(yaml_text)
#         self.assertTrue(isinstance(sampler, RandomSampler))

#         samples = sampler.get_samples()

#         self.assertEqual(len(samples), 5)
#         for sample in samples:
#             self.assertEqual(sample['X1'], 0.5)
#             self.assertTrue(sample['X2'] > 0.2)
#             self.assertTrue(sample['X3'] > 0.2)
#             self.assertTrue(sample['X2'] < 0.8)
#             self.assertTrue(sample['X3'] < 0.8)

#     def test_error1(self):
#         """
#         Given an invalid random specification
#         And I request a new sampler
#         Then I should get a SamplerException
#         """
#         yaml_text = """
#             type: random
#             num_samples: 5
#             #previous_samples: samples.csv # optional
#             constants:
#                 X1: 20
#             parameters:
#                 X2:
#                     min: foo
#                     max: 10
#                 X3:
#                     min: 5
#                     max: 10
#             """
#         with self.assertRaises(SamplingError) as context:
#             new_sampler_from_yaml(yaml_text)
#         self.assertTrue(
#             "must have a numeric minimum"
#             in str(context.exception))

#     def test_error2(self):
#         """
#         Given an invalid random specification
#         And I request a new sampler
#         Then I should get a SamplerException
#         """
#         yaml_text = """
#             type: random
#             num_samples: 5
#             #previous_samples: samples.csv # optional
#             constants:
#                 X1: 20
#             parameters:
#                 X2:
#                     min: 1
#                     max: bar
#                 X3:
#                     min: 5
#                     max: 10
#             """
#         with self.assertRaises(SamplingError) as context:
#             new_sampler_from_yaml(yaml_text)
#         self.assertTrue(
#             "must have a numeric maximum"
#             in str(context.exception))

#     def test_error3(self):
#         """
#         Given previous_samples
#         And I request a new sampler
#         Then I should get a SamplerException
#         """
#         yaml_text = """
#             type: random
#             num_samples: 5
#             previous_samples: samples.csv 
#             constants:
#                 X1: 20
#             parameters:
#                 X2:
#                     min: 1
#                     max: bar
#                 X3:
#                     min: 5
#                     max: 10
#             """
#         with self.assertRaises(SamplingError) as context:
#             new_sampler_from_yaml(yaml_text)
#         self.assertTrue(
#             "'previous_samples' is not yet supported"
#             in str(context.exception))


# class TestScisampleBestCandidate(unittest.TestCase):
#     """
#     Scenario: normal and abnormal tests for BestCandidate
#     """
#     def test_normal(self):
#         """
#         Given a best_candidate specification
#         And I request a new sampler
#         Then I should get a BestCandidate
#         With appropriate values
#         """
#         yaml_text = """
#             type: best_candidate
#             num_samples: 5
#             #previous_samples: samples.csv # optional
#             constants:
#                 X1: 20
#             parameters:
#                 X2:
#                     min: 5
#                     max: 10
#                 X3:
#                     min: 5
#                     max: 10
#             """
#         if PANDAS_PLUS:
#             sampler = new_sampler_from_yaml(yaml_text)
#             self.assertTrue(isinstance(sampler, BestCandidateSampler))
#             samples = sampler.get_samples()

#             self.assertEqual(len(samples), 5)
#             for sample in samples:
#                 self.assertEqual(sample['X1'], 20)
#                 self.assertTrue(sample['X2'] > 5)
#                 self.assertTrue(sample['X3'] > 5)
#                 self.assertTrue(sample['X2'] < 10)
#                 self.assertTrue(sample['X3'] < 10)
#         else:
#             # test only works if pandas is installed
#             self.assertTrue(True)


# class TestCsvSampler(unittest.TestCase):
#     """Unit test for testing the csv sampler."""
#     CSV_SAMPLER = """
#     sampler:
#         type: csv
#         csv_file: {path}/test.csv
#         row_headers: True
#     """

#     # Note: the csv reader does not ignore blank lines
#     CSV1 = """X1,20,20
#     X2,5,10
#     X3,5,10"""

#     def setUp(self):
#         self.tmp_dir = tempfile.mkdtemp()
#         self.definitions = self.CSV_SAMPLER.format(path=self.tmp_dir)
#         self.csv_data = self.CSV1
#         self.sampler_file = os.path.join(self.tmp_dir, "config.yaml")
#         self.csv_file = os.path.join(self.tmp_dir, "test.csv")
#         with open(self.sampler_file, 'w') as _file:
#             _file.write(self.definitions)
#         with open(self.csv_file, 'w') as _file:
#             _file.write(self.csv_data)

#         self.sample_data = read_yaml(self.sampler_file)

#         self.sampler = new_sampler(self.sample_data['sampler'])

#     def tearDown(self):
#         shutil.rmtree(self.tmp_dir, ignore_errors=True)

#     def test_setup(self):
#         self.assertTrue(os.path.isdir(self.tmp_dir))
#         self.assertTrue(os.path.isfile(self.sampler_file))
#         self.assertTrue(os.path.isfile(self.csv_file))

#     def test_dispatch(self):
#         self.assertTrue(isinstance(self.sampler, CsvSampler))

#     def test_samples(self):
#         samples = self.sampler.get_samples()
#         self.assertEqual(len(samples), 2)
#         for sample in samples:
#             self.assertEqual(sample['X1'], 20)
#         self.assertEqual(samples[0]['X2'], 5)
#         self.assertEqual(samples[0]['X3'], 5)
#         self.assertEqual(samples[1]['X2'], 10)
#         self.assertEqual(samples[1]['X3'], 10)

# class TestCustomSampler(unittest.TestCase):
#     """Unit test for testing the custom sampler."""

#     CUSTOM_SAMPLER = """
#         sampler:
#             type: custom
#             function: test_function
#             module: {path}/codepy_sampler_test.py
#             args:
#                 num_samples: 2
#     """

#     CUSTOM_FUNCTION = (
#         """def test_function(num_samples):
#                return [{"X1": 20, "X2": 5, "X3": 5},
#                        {"X1": 20, "X2": 10, "X3": 10}][:num_samples]
#         """)

#     def setUp(self):
#         print("CUSTOM_FUNCTION:\n" + self.CUSTOM_FUNCTION)
#         self.tmp_dir = tempfile.mkdtemp()
#         self.definitions = self.CUSTOM_SAMPLER.format(path=self.tmp_dir)
#         self.function_data = self.CUSTOM_FUNCTION
#         self.sampler_file = os.path.join(self.tmp_dir, "config.yaml")
#         self.function_file = os.path.join(self.tmp_dir,
#                                           "codepy_sampler_test.py")
#         with open(self.sampler_file, 'w') as _file:
#             _file.write(self.definitions)
#         with open(self.function_file, 'w') as _file:
#             _file.write(self.function_data)

#         self.sample_data = read_yaml(self.sampler_file)

#         self.sampler = new_sampler(self.sample_data['sampler'])

#     def tearDown(self):
#         shutil.rmtree(self.tmp_dir, ignore_errors=True)

#     def test_setup(self):
#         self.assertTrue(os.path.isdir(self.tmp_dir))
#         self.assertTrue(os.path.isfile(self.sampler_file))
#         self.assertTrue(os.path.isfile(self.function_file))

#     def test_dispatch(self):
#         self.assertTrue(isinstance(self.sampler, CustomSampler))

#     def test_samples(self):
#         samples = self.sampler.get_samples()
#         self.assertEqual(len(samples), 2)

#         for sample in samples:
#             self.assertEqual(sample['X1'], 20)
#         self.assertEqual(samples[0]['X2'], 5)
#         self.assertEqual(samples[0]['X3'], 5)
#         self.assertEqual(samples[1]['X2'], 10)
#         self.assertEqual(samples[1]['X3'], 10)
