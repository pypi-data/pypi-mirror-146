import unittest

from ffzf import (
    levenshtein_distance,
    jaro_similarity,
    jaro_winkler_similarity,
    hamming_distance
)


class TestScoringFunctions(unittest.TestCase):

    def test_levenshtein_distance(self):
        self.assertEqual(levenshtein_distance("", ""), 0.0)
        self.assertEqual(levenshtein_distance("a", ""), 1.0)
        self.assertEqual(levenshtein_distance("", "a"), 1.0)
        self.assertEqual(levenshtein_distance("a", "a"), 0.0)
        self.assertEqual(levenshtein_distance("a", "b"), 1.0)
        self.assertEqual(levenshtein_distance("b", "a"), 1.0)
        self.assertEqual(levenshtein_distance("a", "ab"), 1.0)
        self.assertEqual(levenshtein_distance("ab", "a"), 1.0)
        self.assertEqual(levenshtein_distance("a", "A"), 0.0)
        self.assertEqual(levenshtein_distance("A", "a", case_sensitive=True), 1.0)
        self.assertEqual(levenshtein_distance("euphoria", "elation"), 7.0)
        self.assertEqual(
            levenshtein_distance("triangle", "abcdefghijklmnopqrstuvwxyz"),
            24.0
        )

    def test_jaro_similarity(self):
        self.assertAlmostEqual(jaro_similarity(
            "subprime", "primers"), 0.779762, places=2)
        self.assertAlmostEqual(jaro_similarity(
            "SubPRIME", "Primers"), 0.779762, places=2)
        self.assertAlmostEqual(jaro_similarity(
            "SUBprime", "prImeRs"), 0.779762, places=2)
        self.assertAlmostEqual(jaro_similarity(
            "codify", "reify"), 0.7, places=2)
        self.assertAlmostEqual(jaro_similarity(
            "absolute", "resolute"), 0.833333, places=2)
        self.assertAlmostEqual(jaro_similarity(
            "anchors", "bank"), 0.595238, places=2)
        self.assertAlmostEqual(jaro_similarity(
            "out", "regaining"), 0.0, places=2)

    def test_jaro_winkler_similarity(self):
        self.assertAlmostEqual(jaro_winkler_similarity(
            "apples", "oranges"), 0.642857, places=2)
        self.assertAlmostEqual(jaro_winkler_similarity(
            "becoming", "trip"), 0.458333, places=2)
        self.assertAlmostEqual(jaro_winkler_similarity(
            "developers", "investment"), 0.532682, places=2)
        self.assertAlmostEqual(jaro_winkler_similarity(
            "trip", "drive"), 0.633333, places=2)
        self.assertAlmostEqual(jaro_winkler_similarity(
            "over", "out"), 0.527778, places=2)

    def test_hamming_distance(self):
        self.assertEqual(hamming_distance("", ""), 0.0)
        self.assertEqual(hamming_distance("ask", "ask"), 0.0)
        self.assertEqual(hamming_distance("men", "hen"), 1.0)
        self.assertEqual(hamming_distance("hello world", "hey there!!"), 9.0)
        
        with self.assertRaises(ValueError):
            hamming_distance("a short string",
                             "a a string longer than a short string")


    def test_scorer_case_sensitive(self):
        self.assertEqual(levenshtein_distance("a", "A", case_sensitive=True), 1.0)
        self.assertEqual(jaro_similarity("a", "A", case_sensitive=True), 0.0)
        self.assertEqual(jaro_winkler_similarity("a", "A", case_sensitive=True), 0.0)
        self.assertEqual(hamming_distance("a", "A", case_sensitive=True), 1.0)

    def test_scorer_remove_whitespac(self):
        self.assertEqual(levenshtein_distance(" \t\na  ", "A", remove_whitespace=True), 0.0)
        self.assertEqual(jaro_similarity(" \t\na  ", "A", remove_whitespace=True), 1.0)
        self.assertEqual(jaro_winkler_similarity(" \t\na  ", "A", remove_whitespace=True), 1.0)
        self.assertEqual(hamming_distance(" \t\na  ", "A", remove_whitespace=True), 0.0)

    def test_scorers_non_ascii(self):
        self.assertEqual(levenshtein_distance("ケーキ", "ケーキ"), 0)
        self.assertEqual(jaro_similarity("ケーキ", "ケーキ"), 1.0)
        self.assertEqual(jaro_winkler_similarity("ケーキ", "ケーキ"), 1.0)
        self.assertEqual(hamming_distance("ケーキ", "ケーキ"), 0)
        self.assertEqual(levenshtein_distance("片付け", "掃討", case_sensitive=True), 3)
        self.assertEqual(jaro_similarity("片付け", "掃討", case_sensitive=True), 0.0)
        self.assertEqual(jaro_winkler_similarity("片付け", "掃討", case_sensitive=True), 0.0)
        
        with self.assertRaises(ValueError):
            hamming_distance("片付け", "掃討", case_sensitive=True)

        self.assertEqual(levenshtein_distance("تنظيف", "清掃", case_sensitive=True), 5)
        self.assertEqual(jaro_similarity("تنظيف", "การทำความสะอาด", case_sensitive=True), 0.0)
        self.assertEqual(jaro_winkler_similarity("تنظيف", "การทำความสะอาด", case_sensitive=True), 0.0)
        self.assertEqual(hamming_distance("सरसफार्इ गर्दै", "การทำความสะอาด", case_sensitive=True), 14)
        self.assertEqual(levenshtein_distance("सरसफार्इ गर्दै", "सरसफार्इ गर्दै", case_sensitive=True), 0)
        self.assertEqual(jaro_similarity("सरसफार्इ गर्दै", "सरसफार्इ   गर्दै", remove_whitespace=True), 1.0)
        
if __name__ == '__main__':
    unittest.main()
