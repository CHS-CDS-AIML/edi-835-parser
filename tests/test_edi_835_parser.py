from tests.conftest import current_path


def test_claim_count(
    blue_cross_nc_sample,
    emedny_sample,
    united_healthcare_legacy_sample,
    gemini_sample,
    all_samples,
):
    assert blue_cross_nc_sample.count_claims() == 1
    assert united_healthcare_legacy_sample.count_claims() == 2
    assert emedny_sample.count_claims() == 3
    assert gemini_sample.count_claims() == 1
    assert all_samples.count_claims() == 7


def test_patient_count(
    blue_cross_nc_sample,
    emedny_sample,
    united_healthcare_legacy_sample,
    gemini_sample,
    all_samples,
):
    assert blue_cross_nc_sample.count_patients() == 1
    assert united_healthcare_legacy_sample.count_patients() == 2
    assert emedny_sample.count_patients() == 3
    assert gemini_sample.count_patients() == 1
    assert all_samples.count_patients() == 7


def test_claim_info(
    gemini_sample
):
    claim_freq_types = list()
    claim_fac_codes = list()

    ts_list = [i for i in gemini_sample]
    for ts in ts_list:
        for claim in ts.claims:
            claim_freq_types.append(claim.claim.claim_freq_type)
            claim_fac_codes.append(claim.claim.claim_facility_code)

    # convert to set
    claim_freq_types = set(claim_freq_types)
    claim_fac_codes = set(claim_fac_codes)

    assert claim_freq_types == set("1")
    assert claim_fac_codes == set([11])


def test_to_dataframe(
    blue_cross_nc_sample,
    emedny_sample,
    united_healthcare_legacy_sample,
    all_samples,
):
    payment = blue_cross_nc_sample.sum_payments()
    blue_cross_nc_data = blue_cross_nc_sample.to_dataframe()

    assert blue_cross_nc_data.shape[0] == 3

    assert payment == blue_cross_nc_data["paid_amount"].sum()

    blue_cross_nc_data.to_csv(f"{current_path}/output/blue_cross_nc_sample.csv")

    payment = emedny_sample.sum_payments()
    emedny_data = emedny_sample.to_dataframe()

    assert emedny_data.shape[0] == 10

    assert payment == emedny_data["paid_amount"].sum()

    emedny_data.to_csv(f"{current_path}/output/emedny_sample.csv")

    payment = united_healthcare_legacy_sample.sum_payments()
    united_healthcare_legacy_ = united_healthcare_legacy_sample.to_dataframe()

    assert united_healthcare_legacy_.shape[0] == 5

    assert payment == united_healthcare_legacy_["paid_amount"].sum()

    united_healthcare_legacy_.to_csv(
        f"{current_path}/output/united_healthcare_legacy_sample.csv"
    )

    payment = all_samples.sum_payments()
    all_data = all_samples.to_dataframe()

    assert round(payment, 2) == all_data["paid_amount"].sum().round(2)

    all_data.to_csv(f"{current_path}/output/all_samples.csv")
