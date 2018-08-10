# Utilities

Some *ad hoc* utilities for analyzing FHIR resources. Requires `msgpack` and `tqdm` packages.

### pack.py

The following scripts use `msgpack` for faster loading of resources (only a few seconds on 1.5M resources). Resources are assumed to be grouped into directories, one resource per JSON file. `pack.py` is used to pack these resources into a single `msgpack`-formatted file.

To pack all resources in a directory named `CARRIER`:

    python pack.py CARRIER


### search.py

Searches all packed resources for all instances of a given key, and returns all found paths along with unique values for the key (and companion key).

To find all instances of `system` and see found `system`/`code` pairs in `CARRIER` resources:

    python search.py system code CARRIER


### analyze.py

Performs some simple analysis of the structure and values within a pack of resources.

To see all requried and optional properties of `extension` elements within `item` elements on `CARRIER` resources:

    $ python analyze.py -d INPATIENT -p item.extension
    Required:
     - url (71)
     - valueQuantity (71)
    Optional:

To see all encountered `url` *values* in `extension` elements of the base resource of `INPATIENT` resources:

    $ python analyze.py -d INPATIENT -p extension -a url
    Required:
     - https://bluebutton.cms.gov/resources/variables/clm_pass_thru_per_diem_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/clm_pps_cptl_dsprprtnt_shr_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/clm_pps_cptl_excptn_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/clm_pps_cptl_fsp_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/clm_pps_cptl_ime_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/clm_pps_cptl_outlier_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/clm_pps_old_cptl_hld_hrmls_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/clm_tot_pps_cptl_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/fi_num (5071)
     - https://bluebutton.cms.gov/resources/variables/nch_bene_blood_ddctbl_lblty_am (5071)
     - https://bluebutton.cms.gov/resources/variables/nch_bene_ip_ddctbl_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/nch_bene_pta_coinsrnc_lblty_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/nch_drg_outlier_aprvd_pmt_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/nch_ip_ncvrd_chrg_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/nch_ip_tot_ddctn_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/nch_profnl_cmpnt_chrg_amt (5071)
     - https://bluebutton.cms.gov/resources/variables/prpayamt (5071)
    Optional:
     - https://bluebutton.cms.gov/resources/variables/clm_mdcr_non_pmt_rsn_cd (78)
     - https://bluebutton.cms.gov/resources/variables/dsh_op_clm_val_amt (2869)
     - https://bluebutton.cms.gov/resources/variables/ime_op_clm_val_amt (2104)
