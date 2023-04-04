from unittest import TestCase
from utils import get_list_of_folders, mkdir_when_not_existent, make_list_of_dirs_in_path, \
    check_if_text_is_a_date_and_output_in_isofromat, get_path_of_a_file_in_a_folder, create_string_with_fill_zeros, \
    remove_non_numeric



class Test(TestCase):
    def test_remove_non_numeric(self):
        self.assertEqual(remove_non_numeric("2007 21 23"),"20072123")
        self.assertEqual(remove_non_numeric("2007-21-23"),"20072123")
        self.assertEqual(remove_non_numeric("2007:21:23"),"20072123")
        self.assertEqual(remove_non_numeric("2007.21.23"),"20072123")
        self.assertEqual(remove_non_numeric("2007 21 23 12 34 56"),"20072123123456")
        self.assertEqual(remove_non_numeric("2007-21-23 hier ist ein random text"),"20072123")

    def test_check_if_text_is_a_date_and_output_in_isofromat(self):
        self.assertEqual(check_if_text_is_a_date_and_output_in_isofromat("20072323"),"")
        self.assertEqual(check_if_text_is_a_date_and_output_in_isofromat("2007 21 23"),"")
        self.assertEqual(check_if_text_is_a_date_and_output_in_isofromat("2007-21-23"),"")
        self.assertEqual(check_if_text_is_a_date_and_output_in_isofromat("2007:21:23"),"")
        self.assertEqual(check_if_text_is_a_date_and_output_in_isofromat("2007.21.23"),"")
        self.assertEqual(check_if_text_is_a_date_and_output_in_isofromat("2007 03 23"),"2007-03-23")
        self.assertEqual(check_if_text_is_a_date_and_output_in_isofromat("2007-03-23"),"2007-03-23")
        self.assertEqual(check_if_text_is_a_date_and_output_in_isofromat("2007:03:23"),"2007-03-23")
        self.assertEqual(check_if_text_is_a_date_and_output_in_isofromat("2007.03.23"),"2007-03-23")
        self.assertEqual(check_if_text_is_a_date_and_output_in_isofromat("2007 03 23 some text"),"2007-03-23")
        self.assertEqual(check_if_text_is_a_date_and_output_in_isofromat("20070323"),"2007-03-23")
        self.assertEqual(check_if_text_is_a_date_and_output_in_isofromat("2007-23-03"),"2007-03-23")