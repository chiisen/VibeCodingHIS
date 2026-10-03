import unittest

from app import app, patients


class PatientRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.original_patients = patients.copy()

    def tearDown(self):
        patients[:] = self.original_patients

    def test_adds_patient_with_valid_form_data(self):
        response = self.client.post(
            "/add_patient",
            data={"name": "測試病人", "age": "25", "gender": "其他"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(patients), len(self.original_patients) + 1)
        self.assertEqual(patients[-1]["name"], "測試病人")

    def test_rejects_gender_outside_allowed_values(self):
        response = self.client.post(
            "/add_patient",
            data={"name": "測試病人", "age": "25", "gender": "invalid"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(patients), len(self.original_patients))
        self.assertIn("請選擇有效的性別", response.get_data(as_text=True))

    def test_rejects_name_longer_than_100_characters(self):
        response = self.client.post(
            "/add_patient",
            data={"name": "甲" * 101, "age": "25", "gender": "男"},
        )

        self.assertEqual(len(patients), len(self.original_patients))
        self.assertIn("姓名不可超過100個字", response.get_data(as_text=True))

    def test_rejects_diagnosis_longer_than_1000_characters(self):
        response = self.client.post(
            "/add_patient",
            data={
                "name": "測試病人",
                "age": "25",
                "gender": "男",
                "diagnosis": "病" * 1001,
            },
        )

        self.assertEqual(len(patients), len(self.original_patients))
        self.assertIn("診斷說明不可超過1000個字", response.get_data(as_text=True))

    def test_unknown_patient_returns_not_found(self):
        response = self.client.get("/patient/unknown-patient-id")

        self.assertEqual(response.status_code, 404)
        self.assertIn("病人不存在", response.get_data(as_text=True))

    def test_missing_page_returns_not_found(self):
        response = self.client.get("/missing-page")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
