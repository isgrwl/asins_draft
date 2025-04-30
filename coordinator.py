'''
    initializes scraper instances and shared data

    note, must install:
        - chrome (.deb works)
        - xvfb (apt works)
        - tkinter (instructions upon running)

'''
import sys
import random
import time
import json
from multiprocessing import Queue, Pool, Process, Manager, TimeoutError
from seleniumbase import SB
from scrape_page import scrape_page, DataRule

# temp
sample_urls = [
    "https://www.amazon.ca/sspa/click?ie=UTF8&spc=MToxNTU1MjQ0ODQ5MTU5NDYxOjE3NDU3OTM5ODQ6c3BfYXRmOjMwMDA1MjA1NTExMDQwMjo6MDo6&url=%2Fall-new-amazon-fire-tv-stick-4k-max%2Fdp%2FB0BXM37848%2Fref%3Dsr_1_1_ffob_sspa%3Fcrid%3D2OVALZ4B5I94I%26dib%3DeyJ2IjoiMSJ9.EQrLpMIzDo7MLJlmVSlTpAWZcBViSRMdeyX790ICqNwoHQ8R2YSlv5tIY342VcKZRaZ9_JCKqcjuoMiQP8X5HJE38epZY7xzXgnuLX5eyx4Zk5_Rs24kJtm9Il-4KGDa5vD0ZcaDjh3AZEpjlAYzTHO1aEq3yJdBjAAs9PGAWU1CSLYvIcTVEV4k06KsxwJikAMAj2OWMxC1hJdUzxF0SfUyBEgjyMg9qhU95NVa7JZnzo5kQ3_0i5GGeLpeC81vZPeWbBuXdAFF50K3eEOsZZtluwoo-52m_33xDX5zVd0.3apLH-mhgLiE5JqdoreI_5avgZ3jnwpHrAcqz7XKP3U%26dib_tag%3Dse%26keywords%3Dtelevision%26qid%3D1745793984%26sprefix%3Dtelevision%252Caps%252C98%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1",
    "https://www.amazon.ca/sspa/click?ie=UTF8&spc=MToxNTU1MjQ0ODQ5MTU5NDYxOjE3NDU3OTM5ODQ6c3BfYXRmOjMwMDUzMDE2MjIyNTkwMjo6MDo6&url=%2Famazon-fire-tv-50-inch-4-series-4k-smart-tv%2Fdp%2FB0CZB5KN7S%2Fref%3Dsr_1_2_ffob_sspa%3Fcrid%3D2OVALZ4B5I94I%26dib%3DeyJ2IjoiMSJ9.EQrLpMIzDo7MLJlmVSlTpAWZcBViSRMdeyX790ICqNwoHQ8R2YSlv5tIY342VcKZRaZ9_JCKqcjuoMiQP8X5HJE38epZY7xzXgnuLX5eyx4Zk5_Rs24kJtm9Il-4KGDa5vD0ZcaDjh3AZEpjlAYzTHO1aEq3yJdBjAAs9PGAWU1CSLYvIcTVEV4k06KsxwJikAMAj2OWMxC1hJdUzxF0SfUyBEgjyMg9qhU95NVa7JZnzo5kQ3_0i5GGeLpeC81vZPeWbBuXdAFF50K3eEOsZZtluwoo-52m_33xDX5zVd0.3apLH-mhgLiE5JqdoreI_5avgZ3jnwpHrAcqz7XKP3U%26dib_tag%3Dse%26keywords%3Dtelevision%26qid%3D1745793984%26sprefix%3Dtelevision%252Caps%252C98%26sr%3D8-2-spons%26ufe%3Dapp_do%253Aamzn1.fos.34134b5b-1573-471e-bd79-624f6072ec84%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1",
    "https://www.amazon.ca/sspa/click?ie=UTF8&spc=MToxNTU1MjQ0ODQ5MTU5NDYxOjE3NDU3OTM5ODQ6c3BfYXRmOjMwMDYxMDI5NjI2NTIwMjo6MDo6&url=%2FFPD-Google-Screen-Palette-CG43-P3%2Fdp%2FB0CRRRMK5W%2Fref%3Dsr_1_3_sspa%3Fcrid%3D2OVALZ4B5I94I%26dib%3DeyJ2IjoiMSJ9.EQrLpMIzDo7MLJlmVSlTpAWZcBViSRMdeyX790ICqNwoHQ8R2YSlv5tIY342VcKZRaZ9_JCKqcjuoMiQP8X5HJE38epZY7xzXgnuLX5eyx4Zk5_Rs24kJtm9Il-4KGDa5vD0ZcaDjh3AZEpjlAYzTHO1aEq3yJdBjAAs9PGAWU1CSLYvIcTVEV4k06KsxwJikAMAj2OWMxC1hJdUzxF0SfUyBEgjyMg9qhU95NVa7JZnzo5kQ3_0i5GGeLpeC81vZPeWbBuXdAFF50K3eEOsZZtluwoo-52m_33xDX5zVd0.3apLH-mhgLiE5JqdoreI_5avgZ3jnwpHrAcqz7XKP3U%26dib_tag%3Dse%26keywords%3Dtelevision%26qid%3D1745793984%26sprefix%3Dtelevision%252Caps%252C98%26sr%3D8-3-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1",
    "https://www.amazon.ca/sspa/click?ie=UTF8&spc=MToxNTU1MjQ0ODQ5MTU5NDYxOjE3NDU3OTM5ODQ6c3BfYXRmOjMwMDcyNDI3MDUxNzUwMjo6MDo6&url=%2FSAMSUNG-32-Inch-720p-Smart-PurColour%2Fdp%2FB0DXQQRG8C%2Fref%3Dsr_1_4_sspa%3Fcrid%3D2OVALZ4B5I94I%26dib%3DeyJ2IjoiMSJ9.EQrLpMIzDo7MLJlmVSlTpAWZcBViSRMdeyX790ICqNwoHQ8R2YSlv5tIY342VcKZRaZ9_JCKqcjuoMiQP8X5HJE38epZY7xzXgnuLX5eyx4Zk5_Rs24kJtm9Il-4KGDa5vD0ZcaDjh3AZEpjlAYzTHO1aEq3yJdBjAAs9PGAWU1CSLYvIcTVEV4k06KsxwJikAMAj2OWMxC1hJdUzxF0SfUyBEgjyMg9qhU95NVa7JZnzo5kQ3_0i5GGeLpeC81vZPeWbBuXdAFF50K3eEOsZZtluwoo-52m_33xDX5zVd0.3apLH-mhgLiE5JqdoreI_5avgZ3jnwpHrAcqz7XKP3U%26dib_tag%3Dse%26keywords%3Dtelevision%26qid%3D1745793984%26sprefix%3Dtelevision%252Caps%252C98%26sr%3D8-4-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1",
    "https://www.amazon.ca/Hisense-32A4KV-Smart-TruSurround-Canada/dp/B0BSXW2HJD/ref=sr_1_5?crid=2OVALZ4B5I94I&dib=eyJ2IjoiMSJ9.EQrLpMIzDo7MLJlmVSlTpAWZcBViSRMdeyX790ICqNwoHQ8R2YSlv5tIY342VcKZRaZ9_JCKqcjuoMiQP8X5HJE38epZY7xzXgnuLX5eyx4Zk5_Rs24kJtm9Il-4KGDa5vD0ZcaDjh3AZEpjlAYzTHO1aEq3yJdBjAAs9PGAWU1CSLYvIcTVEV4k06KsxwJikAMAj2OWMxC1hJdUzxF0SfUyBEgjyMg9qhU95NVa7JZnzo5kQ3_0i5GGeLpeC81vZPeWbBuXdAFF50K3eEOsZZtluwoo-52m_33xDX5zVd0.3apLH-mhgLiE5JqdoreI_5avgZ3jnwpHrAcqz7XKP3U&dib_tag=se&keywords=television&qid=1745793984&sprefix=television%2Caps%2C98&sr=8-5&ufe=app_do%3Aamzn1.fos.a9cfdadb-853e-427d-a2b7-ed306eff4f60",
    "https://www.amazon.ca/LG-43-Inch-UT7000-Smart-43UT7000PUA/dp/B0DDDYJ7FJ/ref=sr_1_6?crid=2OVALZ4B5I94I&dib=eyJ2IjoiMSJ9.EQrLpMIzDo7MLJlmVSlTpAWZcBViSRMdeyX790ICqNwoHQ8R2YSlv5tIY342VcKZRaZ9_JCKqcjuoMiQP8X5HJE38epZY7xzXgnuLX5eyx4Zk5_Rs24kJtm9Il-4KGDa5vD0ZcaDjh3AZEpjlAYzTHO1aEq3yJdBjAAs9PGAWU1CSLYvIcTVEV4k06KsxwJikAMAj2OWMxC1hJdUzxF0SfUyBEgjyMg9qhU95NVa7JZnzo5kQ3_0i5GGeLpeC81vZPeWbBuXdAFF50K3eEOsZZtluwoo-52m_33xDX5zVd0.3apLH-mhgLiE5JqdoreI_5avgZ3jnwpHrAcqz7XKP3U&dib_tag=se&keywords=television&qid=1745793984&sprefix=television%2Caps%2C98&sr=8-6",
    "https://www.amazon.ca/introducing-amazon-fire-tv-32-inch-2-series-hd-smart-tv/dp/B09N6XYRK7/ref=sr_1_7?crid=2OVALZ4B5I94I&dib=eyJ2IjoiMSJ9.EQrLpMIzDo7MLJlmVSlTpAWZcBViSRMdeyX790ICqNwoHQ8R2YSlv5tIY342VcKZRaZ9_JCKqcjuoMiQP8X5HJE38epZY7xzXgnuLX5eyx4Zk5_Rs24kJtm9Il-4KGDa5vD0ZcaDjh3AZEpjlAYzTHO1aEq3yJdBjAAs9PGAWU1CSLYvIcTVEV4k06KsxwJikAMAj2OWMxC1hJdUzxF0SfUyBEgjyMg9qhU95NVa7JZnzo5kQ3_0i5GGeLpeC81vZPeWbBuXdAFF50K3eEOsZZtluwoo-52m_33xDX5zVd0.3apLH-mhgLiE5JqdoreI_5avgZ3jnwpHrAcqz7XKP3U&dib_tag=se&keywords=television&qid=1745793984&sprefix=television%2Caps%2C98&sr=8-7&ufe=app_do%3Aamzn1.fos.15985262-82f3-4da3-a391-5bcc87a1e788",
    "https://www.amazon.ca/sspa/click?ie=UTF8&spc=MTo4NjQ0MjYxMTY4MDU5NDA0OjE3NDU3OTM5ODQ6c3Bfc2VhcmNoX3RoZW1hdGljOjMwMDQ1MjIxNDc3MTAwMjo6MDo6&url=%2FSamsung-UN32M4500BFXZC-Smart-Canada-Version%2Fdp%2FB07FGHK2C9%2Fref%3Dsxin_15_pa_sp_search_thematic_sspa%3Fcontent-id%3Damzn1.sym.99c74ff6-4df9-4910-9de7-a62eedd7f3b0%253Aamzn1.sym.99c74ff6-4df9-4910-9de7-a62eedd7f3b0%26crid%3D2OVALZ4B5I94I%26cv_ct_cx%3Dtelevision%26keywords%3Dtelevision%26pd_rd_i%3DB07FGHK2C9%26pd_rd_r%3D0aa410c3-e80c-490d-b8bd-2720b44271df%26pd_rd_w%3DBh3U2%26pd_rd_wg%3DUYCDX%26pf_rd_p%3D99c74ff6-4df9-4910-9de7-a62eedd7f3b0%26pf_rd_r%3DMNF74XMEJMG0FTDST0WK%26qid%3D1745793984%26sbo%3DRZvfv%252F%252FHxDF%252BO5021pAnSA%253D%253D%26sprefix%3Dtelevision%252Caps%252C98%26sr%3D1-1-0db4faf6-3485-4ed7-80e2-7395e0b5d027-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM%26psc%3D1",
    "https://www.amazon.ca/sspa/click?ie=UTF8&spc=MTo4NjQ0MjYxMTY4MDU5NDA0OjE3NDU3OTM5ODQ6c3Bfc2VhcmNoX3RoZW1hdGljOjMwMDYwMzc3ODI5OTQwMjo6MTo6&url=%2FPANMILED-JL-D580A1330-365AS-M_V02-H58AE6100UK-HD580S1U02-HD580S1U91%2Fdp%2FB0B3HYPV6J%2Fref%3Dsxin_15_pa_sp_search_thematic_sspa%3Fcontent-id%3Damzn1.sym.99c74ff6-4df9-4910-9de7-a62eedd7f3b0%253Aamzn1.sym.99c74ff6-4df9-4910-9de7-a62eedd7f3b0%26crid%3D2OVALZ4B5I94I%26cv_ct_cx%3Dtelevision%26keywords%3Dtelevision%26pd_rd_i%3DB0B3HYPV6J%26pd_rd_r%3D0aa410c3-e80c-490d-b8bd-2720b44271df%26pd_rd_w%3DBh3U2%26pd_rd_wg%3DUYCDX%26pf_rd_p%3D99c74ff6-4df9-4910-9de7-a62eedd7f3b0%26pf_rd_r%3DMNF74XMEJMG0FTDST0WK%26qid%3D1745793984%26sbo%3DRZvfv%252F%252FHxDF%252BO5021pAnSA%253D%253D%26sprefix%3Dtelevision%252Caps%252C98%26sr%3D1-2-0db4faf6-3485-4ed7-80e2-7395e0b5d027-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM%26psc%3D1",
    "https://www.amazon.ca/sspa/click?ie=UTF8&spc=MTo4NjQ0MjYxMTY4MDU5NDA0OjE3NDU3OTM5ODQ6c3Bfc2VhcmNoX3RoZW1hdGljOjMwMDQ1MjIxNDc3MTMwMjo6Mjo6&url=%2FSAMSUNG-Processor-Tracking-Q-Symphony-Upscaling%2Fdp%2FB0CY18SS15%2Fref%3Dsxin_15_pa_sp_search_thematic_sspa%3Fcontent-id%3Damzn1.sym.99c74ff6-4df9-4910-9de7-a62eedd7f3b0%253Aamzn1.sym.99c74ff6-4df9-4910-9de7-a62eedd7f3b0%26crid%3D2OVALZ4B5I94I%26cv_ct_cx%3Dtelevision%26keywords%3Dtelevision%26pd_rd_i%3DB0CY18SS15%26pd_rd_r%3D0aa410c3-e80c-490d-b8bd-2720b44271df%26pd_rd_w%3DBh3U2%26pd_rd_wg%3DUYCDX%26pf_rd_p%3D99c74ff6-4df9-4910-9de7-a62eedd7f3b0%26pf_rd_r%3DMNF74XMEJMG0FTDST0WK%26qid%3D1745793984%26sbo%3DRZvfv%252F%252FHxDF%252BO5021pAnSA%253D%253D%26sprefix%3Dtelevision%252Caps%252C98%26sr%3D1-3-0db4faf6-3485-4ed7-80e2-7395e0b5d027-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM%26psc%3D1",
    "https://www.amazon.ca/sspa/click?ie=UTF8&spc=MTo4NjQ0MjYxMTY4MDU5NDA0OjE3NDU3OTM5ODQ6c3Bfc2VhcmNoX3RoZW1hdGljOjMwMDczMzA1ODQyOTcwMjo6Mzo6&url=%2FBacklight-55LB650V-55LB561V-55LF6000-55LB6100%2Fdp%2FB09ZNMPWNZ%2Fref%3Dsxin_15_pa_sp_search_thematic_sspa%3Fcontent-id%3Damzn1.sym.99c74ff6-4df9-4910-9de7-a62eedd7f3b0%253Aamzn1.sym.99c74ff6-4df9-4910-9de7-a62eedd7f3b0%26crid%3D2OVALZ4B5I94I%26cv_ct_cx%3Dtelevision%26keywords%3Dtelevision%26pd_rd_i%3DB09ZNMPWNZ%26pd_rd_r%3D0aa410c3-e80c-490d-b8bd-2720b44271df%26pd_rd_w%3DBh3U2%26pd_rd_wg%3DUYCDX%26pf_rd_p%3D99c74ff6-4df9-4910-9de7-a62eedd7f3b0%26pf_rd_r%3DMNF74XMEJMG0FTDST0WK%26qid%3D1745793984%26sbo%3DRZvfv%252F%252FHxDF%252BO5021pAnSA%253D%253D%26sprefix%3Dtelevision%252Caps%252C98%26sr%3D1-4-0db4faf6-3485-4ed7-80e2-7395e0b5d027-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM%26psc%3D1",
    "https://www.amazon.ca/sspa/click?ie=UTF8&spc=MTo4NjQ0MjYxMTY4MDU5NDA0OjE3NDU3OTM5ODQ6c3Bfc2VhcmNoX3RoZW1hdGljOjMwMDQ1MjIxNDc3MTEwMjo6NDo6&url=%2FSamsung-UN32N5300AFXZC-Glossy-Canada-Version%2Fdp%2FB07DW7F2FM%2Fref%3Dsxin_15_pa_sp_search_thematic_sspa%3Fcontent-id%3Damzn1.sym.99c74ff6-4df9-4910-9de7-a62eedd7f3b0%253Aamzn1.sym.99c74ff6-4df9-4910-9de7-a62eedd7f3b0%26crid%3D2OVALZ4B5I94I%26cv_ct_cx%3Dtelevision%26keywords%3Dtelevision%26pd_rd_i%3DB07DW7F2FM%26pd_rd_r%3D0aa410c3-e80c-490d-b8bd-2720b44271df%26pd_rd_w%3DBh3U2%26pd_rd_wg%3DUYCDX%26pf_rd_p%3D99c74ff6-4df9-4910-9de7-a62eedd7f3b0%26pf_rd_r%3DMNF74XMEJMG0FTDST0WK%26qid%3D1745793984%26sbo%3DRZvfv%252F%252FHxDF%252BO5021pAnSA%253D%253D%26sprefix%3Dtelevision%252Caps%252C98%26sr%3D1-5-0db4faf6-3485-4ed7-80e2-7395e0b5d027-spons%26ufe%3Dapp_do%253Aamzn1.fos.a9cfdadb-853e-427d-a2b7-ed306eff4f60%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM%26psc%3D1",
    "https://www.amazon.ca/SAMSUNG-Processor-Tracking-Q-Symphony-Upscaling/dp/B0CY145P43/ref=sr_1_8?crid=2OVALZ4B5I94I&dib=eyJ2IjoiMSJ9.EQrLpMIzDo7MLJlmVSlTpAWZcBViSRMdeyX790ICqNwoHQ8R2YSlv5tIY342VcKZRaZ9_JCKqcjuoMiQP8X5HJE38epZY7xzXgnuLX5eyx4Zk5_Rs24kJtm9Il-4KGDa5vD0ZcaDjh3AZEpjlAYzTHO1aEq3yJdBjAAs9PGAWU1CSLYvIcTVEV4k06KsxwJikAMAj2OWMxC1hJdUzxF0SfUyBEgjyMg9qhU95NVa7JZnzo5kQ3_0i5GGeLpeC81vZPeWbBuXdAFF50K3eEOsZZtluwoo-52m_33xDX5zVd0.3apLH-mhgLiE5JqdoreI_5avgZ3jnwpHrAcqz7XKP3U&dib_tag=se&keywords=television&qid=1745793984&sprefix=television%2Caps%2C98&sr=8-8",
    "https://www.amazon.ca/Hisense-55A68N-Vision-Google-Bluetooth/dp/B0CW2FV2KJ/ref=sr_1_9?crid=2OVALZ4B5I94I&dib=eyJ2IjoiMSJ9.EQrLpMIzDo7MLJlmVSlTpAWZcBViSRMdeyX790ICqNwoHQ8R2YSlv5tIY342VcKZRaZ9_JCKqcjuoMiQP8X5HJE38epZY7xzXgnuLX5eyx4Zk5_Rs24kJtm9Il-4KGDa5vD0ZcaDjh3AZEpjlAYzTHO1aEq3yJdBjAAs9PGAWU1CSLYvIcTVEV4k06KsxwJikAMAj2OWMxC1hJdUzxF0SfUyBEgjyMg9qhU95NVa7JZnzo5kQ3_0i5GGeLpeC81vZPeWbBuXdAFF50K3eEOsZZtluwoo-52m_33xDX5zVd0.3apLH-mhgLiE5JqdoreI_5avgZ3jnwpHrAcqz7XKP3U&dib_tag=se&keywords=television&qid=1745793984&sprefix=television%2Caps%2C98&sr=8-9",
]

rules = [
    DataRule("title", '#productTitle'),
    DataRule("price", '#corePriceDisplay_desktop_feature_div .aok-offscreen'),
    DataRule("stars", '#acrPopover .a-icon-alt'),
    DataRule("bought_past_month",
             '#social-proofing-faceout-title-tk_bought')
]


def main():
    # defaults (should replace with cmdline args)
    OUTFILE = "data.json"
    NUM_INSTANCES = 3
    TYPE = scrape_page

    # initialization
    manager = Manager()
    results = manager.dict()  # scraper results (shared)
    urls = Queue()  # urls to scrape (shared)

    # temp
    for u in sample_urls:
        urls.put(u)

    instances = []

    # spawn multiple scraper instances
    for instance_num in range(NUM_INSTANCES):
        instance = Process(
            target=run_scraper,
            args=(urls, results, instance_num+1, TYPE)
        )
        instance.start()
        instances.append(instance)
        print(f"Spawned instance {instance_num}")

    # wait for all processes to complete
    for instance in instances:
        instance.join()
        print(f"Instance exited")

    # store data in json
    with open(OUTFILE, "w+") as f:
        temp = results.copy()
        json.dump(temp, f)
        print(f"\nWrote {len(temp)} records to {OUTFILE}.")


# initialize scraper and begin processing URLs with getData callback
def run_scraper(urls, results, instance_num, getData=None,):
    with SB(
        uc=True,
        xvfb=False,
        headed=True,
        ad_block=True,
        page_load_strategy="eager",
        skip_js_waits=True,
        # block_images=True,
        # disable_js=True,
    ) as sb:
        sb.activate_cdp_mode()

        while True:
            try:
                url = urls.get(True, 3)  # get url from queue
                page = sb.cdp.get(url)  # navigate to url
                data = getData(sb,rules)  # run callback with browser context
                results[url] = data  # store result

            except Exception as error:
                # no urls left, close instance
                print(error)
                print(f"Nothing left to scrape in instance {instance_num}")
                return


if __name__ == "__main__":
    main()
