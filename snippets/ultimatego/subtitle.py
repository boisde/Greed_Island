#!/usr/bin/env python3.7

import os
import subprocess
import shutil


info = {
    # "18-3.2_Mechanical_Sympathy":["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_6ofosdtz/segmentDuration/300/ks/djJ8MTkyNjA4MXwL8u7PVpIk4cpFOOkx5WdfwKR0Og8wCGm00hbBrIbibaDkgsjYEYmY6IOq77ojZY-5yO0NqCFjF-Hc2w9wESqe5-En0JUlfi1tvY_p3ViF8oORdWTJg3h1o8ClYC6ynHAlgKfdMVpKiAaVZwqfu8db6LB8HZweQGzTigwVYyngec4i0oBpmRTz3JFfiA_mMY7D0oXit4rGicw9YVhU4Mqmyq-2FZljErwOw0W3E825iyqifANUbGrnuus0aSI2br_BkDZNmEMTnYS1E5WqQkiX/version/32/a.m3u8", ""],
    # "19-3.2_Semantics": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_fgvlpwnt/segmentDuration/300/ks/djJ8MTkyNjA4MXzpjtde1WndjPXYBSzaNzslcX4y-M72JBLbBHX2oICEUbZ8bqwrFI-sGp__jo8HsGrNaVrwlWn4wSzO5qkn72efG4jTFVDcg90aNHNwkvbgoYIWkv9bUSUUa28ltQ9aXPCERyvrOk-k4acCStwhtO5hUJAQdKrZICfEy0WVnjnrJJClwbjZLcQWJJIrlFOmDBcDa5UuXmXpcve0Fl8vVfHXSssY5g6lrWc4mJ9txGu9Kfi4NLNAxxmssu2WHtMmpoRAGf7D8tW75Bfqvy4Xht42/version/42/a.m3u8", ""],
    # "20-3.3_Declare_and_Length_and_Reference_Types": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_ydczen5e/segmentDuration/300/ks/djJ8MTkyNjA4MXxW_MIMisG12ozaUGQtwDPl5mOE3jKZGSwpV4L_5FhMQtYalyJ-Ro76TgvN6_LWHTJylx1qCSjV0xeT206hOUijGKwiO14sc4KMtp37aWdoXe64noPz3Cwli-BPXmAKXO7fjP432qatOzx1GxUpBhcMDsmxkVgym5Gt31C-ZR4TpsOIqfEQK4ZhT_r01Bjfgd_kOqqYtQ-lNMSUsdoKlRc6jg8CCS5Yveh-1ad07pXf7HHjo8ErnYNEvKu73wotZLB-EftdAT1w0mAUY5wF8Twg/version/32/a.m3u8", ""],
    # "21-3.3_Appending_Slices": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_jv5p8bb9/segmentDuration/300/ks/djJ8MTkyNjA4MXyaQ3lf381fRTfOGflvopQwxK70acvU9sMhyGHwu9ohscdxyj0YCJZVRAW4j6G6Uyi-sTfwKH-_SxvL7SpyCUlywwr6VzlwSQE9H6Qe0BBx7S1gnzEebuVFvHxvPvBMZGUW6C9tD78ckRp0018zwMXgHh0Ozpjeqorhoh0PmuTXw4HkkcvDIftqSoW64fWzocjUfA3_FpjeHy5tLwCpB4yf22ayHFdv6v_j4j6Tk1Sd06JuZp7_TPwFGsErUoi384o6MEcesxD1FD9ebxlFSAJV/version/42/a.m3u8",""],
    # "22-3.3_Taking_Slices_of_Slices": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_63n5f1wq/segmentDuration/300/ks/djJ8MTkyNjA4MXxQEPN9amNfWDUX-qp_WVoMsrRn1v2hx6Wf55PcruyzFR7i5qsH7XKCRqmUsNO7ODDArM641GrsHWeWt2qMCNWg9KpwnjOMfERYXPdeoHvdRSMLit3ufR-d5ouLm7yGg9NQKYdtWRRaSqJJTl9wqyS1Z6TnlPu9h2GKQ22fOjuaZpJv_B7AiuyLFflk3sySEMMgZJ-0maM7kbdIcatI4UF_3ZxOQlkPVJkHo7f8OJjgHm6u7EY1hDk6ylUIPcgR2C8VrYO_kbJzqXYv5bNYftFE/version/42/a.m3u8", ""],
    # "23-3.3_Slices_and_References": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_s3bv0w3r/segmentDuration/300/ks/djJ8MTkyNjA4MXxsj4AXwdoo9G4BIG2Zz9gx218zI8yk6BfPeDA0XAdwQXa2UtLsIRZmJ2fecfm3J3WGwb_6IpcOrPGWaaAfJtIhxyPcVC5wEmslwoj-hSoH1r9oHitadCZSExGzmR8mjMzShJLwBYTJ7sbDtP6Tp2gHqiKPJsIlbZrTcKWdzfqPbSk-u03e14zs0NjDgn9ABIxhiuzk4Xyn7HMAW_r5qaTgUnlYxAls8zFBUCWRHhT2Q45mylZ4u0APLuds8DRzMd1i7pKiZZla_P0UgF6p7_wz/version/52/a.m3u8", ""],
    # "24-3.3_Strings_and_Slices": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_38t69uae/segmentDuration/300/ks/djJ8MTkyNjA4MXx85dJk5FGXWMf_mc4H0FiBtWj9m69ymhyxGaBXyi7elv_Ji3svEE0a3PsDu6pAFTtykSprwYhkf2Erk8n8rx0KeKlUyCAW9JStYB6YGCN_YivBr8yYe7arSo0nEHkEV4pQLx8tBbXPI8gDlvs3MnHeqwH04NJT0lLHG0Lv1pHDFe1j0KHfNzapUB3yZhnfAp5xKsG_V9Mw34x_zi6RUvvaJKWnrhs0uhJK6vjRQmbcmpKMR9Pflk5oQ2vcDB-SGrTrNV0qYaxWr6a_wuunUar4/version/32/a.m3u8", ""],
    # "25-3.3_Range_Mechanics": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_j69nml0v/segmentDuration/300/ks/djJ8MTkyNjA4MXyEkD2cK2xjVOvpogl8GXBZIA9_iuBloJrLdkWNljAOpFHLmh4EdL4mI7tv1PxaFMOX2HtCRsDz-5CIzkYsHjLPvrj6wD_NVt7wpxXnPMCPGWLIGZVyCgSOqL-Qg3uL0_s0wKlvtnDO1y8YElE7Uc-LudQu2Or5HTM2G_8ytDhBMXQNN6zhF-dU4mBeYB9KWz6ERXpJSPGQoYx3Uso9jUj2HZxixa3xDNdF_otvReodlQ0XY5LQqbwvvDJEaxwtBRA3Jg6rFKEb5majbUCo-Udl/version/42/a.m3u8", ""],
    # "26-3.4_Maps":["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_25ts55ls/segmentDuration/300/ks/djJ8MTkyNjA4MXzfMwe0aFILqWyEp5GdSeFU8NYF-mteaHtxA-OE6-FKC4XrMcQLm5diGUOs8nNCqI20nXkSx9VOkEWIFMHDY1gH1olAvTPuvNrh4S1jRct8TBgAJwvzkfoWLwD-sGAED7awh1Lp1da1WGrJOp-nVr9SltCzTTsUZM9zDoqPVcU3QFa7ePaK4Uokcv9wuRLXFcmk3iDlifJr2q-Fy_yek4VyMQfJBd4-NlUp0l9krPyaeKrkZxw1KF0PgGwSv3hYQf5nbH_L_ffIG13FkKk3gnyh/version/42/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_lam4it19/v/2/ev/11/flavorId/0_6qjsfgog/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX2xhbTRpdDE5L3YvMi9ldi8xMSoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE1Nzc1NTk0NjR9fX1dfQ__&Signature=Qy0wgTC1iQdYCpYbIxhHMLhEG3EgTHJa2bIb3pnXmYSa32Gz42l7CwbURLUCpxCmVG81CO6R5IvJvb-RKdAtwbPwjEmW6FE2RXgEYPJpaMGxjNJqnGsxbbX3RA7c9O8FzJxX2olmd5dlOepovz7NDx0hzLOSYLaQhnOFQ5fo-quZ7sm0z47aWuMzESdSjyT3xY9JkrXgpJTB-zThFsUgj--yCVetVk-L3NN2JdwUUXV7ZOEFgyy8wkOGUcvfuj4IGQ9Kv31r0H8xAuzNpP2Z9-LEKrXc0HpOafJnL-B39ijYQNG7qSTfuP9gFkwQGJ5NejcHQtWk48KAl617dfNYuA__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "27-4.0_Topics":["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_mn0p52r8/segmentDuration/300/ks/djJ8MTkyNjA4MXzRvNIlCqKuOI38VvLTR8p-y24xAB2qmTtm6qEFK5O3uwxxfGvXXhfGenkZeKKu3FPW5JOf9uYTogQZruLD2I940J_pSjSUlX22D5Yy3Ydh5kQXpq9pj7-T3Mrn7BR9woXGcCIRHp2c8TR3zR19lLhR0cy3squ5A7hfTso0-wYHB-7J-CNlvkfzHadeCiDQ6DnwZJSSRccx6RiBcGMAxexCdiC5IqearjqzCDfkTyt7FzojliG2zFqRv-MGvskEb98r1-1L82YMxebO80J6CXqw/version/42/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_fq9nwxml/v/12/ev/18/flavorId/0_t6w2wg55/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX2ZxOW53eG1sL3YvMTIvZXYvMTgqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTgzMTYyMjk1fX19XX0_&Signature=NSW4tI0Wv0bTbInYtzlRqMJuMvt8s4zvHV5Z9XEqhwA1tEMBpPkajg6DjLaekUYSQdA9nZQwSxMMypn67imz-m8tBa0y351AfkPoyomnw5ZdXL0hMbLkbKK7ckTioDecHnf3nXQVcmUxUzxCmBRmAQU7pjiDQY1IKKkj1lbD~bxQpWjATCJtvPw0IAmU3KehkfDTyMLPSywnLe58EKu5sWgMLhmuOhTMI2sk-EKxxiz9lnJm58zpRZFpRICcxnmkghg1BvL8xGhALg-KTvyDamJHAVEftOmfiljqUP4aQXVjkrURpFUyBRtX9TSPNtTnpClNt8LOSqTx8d922sk3ew__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "28-4.1_Declare_and_Receiver_Behavior": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_ese600d3/segmentDuration/300/ks/djJ8MTkyNjA4MXxsoSTUEjMYt3l0lUY0EKLfMkdRRiqut5iWLUeyO88Quc7bh5l7L4YqqWLAvP9ga71PdKDfG0_ugc9HpQ3rDjcDnP_WigaaiC0Ka3TwxdNtME-UA1_RMaiELVxengMh9ua31NEwPOOmzZliU7V9HXGQJFONfA-u9aJ1VIZeca-y6UyC5hJkPOj5XTR2Eul7AzeeiIJE4epECR_kxwN3LOsDbLficxdxyMBeb89FQwqgisjHEYue21cE0ILyP-bSAEHH0sDQD0xpbUi4ttSifyJI/version/42/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_5mi99gp7/v/12/ev/18/flavorId/0_1mio9y59/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wXzVtaTk5Z3A3L3YvMTIvZXYvMTgqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTgzMTYxNjE1fX19XX0_&Signature=P-LBc5c-pu~WFh0kORpB8mj9INaQvjW9lBCXJv-P97ibBwqKYuyFbKt2Z9JfZtLYeQm3TOEv-JnCGagpzcNAoukJXKFYIrLVKsXE20X4SfZ6yhTdLCyPuyk6A9o5p67UZZ13YnDpQWjsWnsoYZbdsp9sXA2Djwu49Hz-irst9PLEYewqQHcaN~DrvPcPZkz5TIDJOZPgjmajFrJEIZY6UD8023J5NmhbBnJ~NcdZSGeenZkJHjcdx-8s1XLbC1tPK-jqcyuT8H~dvS5V3qm0BHFsqzC~xxx8jIteiEXrhv0CE28yrckGPEHvnz1y-5QOO4KhVA0bIkKgz2Kb1exSMw__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "29-4.1_Value_and_Pointer_Semantics": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_hzrgqz91/segmentDuration/300/ks/djJ8MTkyNjA4MXyVw7YbLTWeDzDEAjk9Z923fL_9zdAIvPYUiPoiCzoC4bD97rRBQTg91tdxwFeTPTaXT0EpJXHrk5c4XBM4DBJ6saicyDA9ZsjI8zyS2SgEF6HuvO61gbZ37SCok49LULZfA2w-oNDDdQPLWEH-X4VIFUqcrrb4IiP5ENri3npHt2ns5W1XedMs6omlLSCKe_81e4jf4ZaZaTVc6UHNPUPTKxjTQkKFjIdXp_PInguo-pxL3lWOUq8-0Yjg8gWY1TEi1R2DthdmMWxjtkl206jw/version/42/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_1sevjnzb/v/12/ev/18/flavorId/0_tlwtsv0a/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wXzFzZXZqbnpiL3YvMTIvZXYvMTgqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTgzMTYyNDQxfX19XX0_&Signature=ag4TUu1hes0CXOzfkcw2FAPaY1t4S0rxK4ScGalKzs1xMTKjkNnjyi2p0ARaFibLJrqHl2VYTSbiR1ipP2ktjOmIWJNIqnTOQPz49V3MZpkGNuH3xxQHRCC5oULqbhSc-Eae1lx-WoApgSwTLp2q22Cu6OXW1Lab4ZbW~~~aZ8nVZvgoo4T~Oy9FxjebORg72qiRDsNZQx2Pt4JEQ-CX3VymlSk-KockApJdvQwfT7nGSLDYdCdUQGIiZxuyEBTjL-p8y9uCCku3c8RT3b3ZvR~UhHf6fsXi1r7cDPDRdJhV8xreO8P-PKoGhBFu5SjbCNcL7V9Axxg-SmAy7TD6IA__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    "14.4_P2_Macro_Level_Optimization_Memory_Profiing": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_hu3vtuno/segmentDuration/300/ks/djJ8MTkyNjA4MXyDA8aFq9LDRUOS2bdKolQxDbrdYDD0vWkiOCchVZoqKJ3n4qOVOdnn1aMiGD6Dg8BSE3wyTJnFylVewUx3QRgO7ENmTGdFF5l4lG_d7p47n89X8NdMrlEAoBqy4A0amfHT128MP8woLqcAOsby_nremB73ZyX-ZGoV2YmBYAOl-Hkl2_upksxb4kzADZCdhfNazKZtrPcvsD9C0ZWZHIMWaQQH8JsQjQd3_qZzEL7uCWkD_F3p4cFiu6D_sFKcN7zHa1cYrGCo2iHGsl9ujv72/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_r9gx765m/v/12/ev/21/flavorId/0_4iq9v4v6/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX3I5Z3g3NjVtL3YvMTIvZXYvMjEqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk2MDM2NjUzfX19XX0_&Signature=HfGfKmpNqHb6GQ1Kcy7Jauvz9c3SsMaouhUwZBC9GB6wDFpYa8bePmEhvMUwx1gPTh5HGLh~tzzYhLmZSXRHDxH~01tAp8nbKWn00JAai6ghL02AtyFCnf59pUX-XcQPhWKr~GlfYwqu-JpI8mnrV~Pa3bBs89qHliE7YsWltVJHHfwwXnavr5Vx5jOSD~UIyRyGi-Jr5d5cDq5r~PBML56dRgTy7BUz0NR5bLWCgcCb93hUTYVy5oD79s2JpTHAUes9pCTxWzd7YmOHkhhSO5fS2YjhhwC3-ZomBn0TwLTuLGozbXF41496BEooczU1lwbg5tYfbmtx79jnD50bxw__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "xxx": [],
}


CUR_PATH = os.path.abspath(".")


def do():
    print(MP4)
    print(ASS)
    print(OUT_MP4)

    # m3u8 to mp4
    c = "ffmpeg -i \"%s\" -c copy -bsf:a aac_adtstoasc %s" % (M3U8_URL, MP4)
    print("\n", c, "\n")
    subprocess.check_call(c, stderr=subprocess.STDOUT, shell=True)
    print()

    # m3u8 to vtt files
    c = "ffmpeg -i \"%s\" -f segment -segment_time 300 -segment_format webvtt -scodec copy %s" % (SUB_URL, SUB_FILE_NAME_PATTERN)
    print("\n", c, "\n")
    subprocess.check_call(c, stderr=subprocess.STDOUT, shell=True)
    print()
    
    # vtt to ass
    subs = []
    for (_dirpath, _dirnames, filenames) in os.walk(CUR_PATH):
        for filename in filenames:
            if filename.startswith("sub-"):
                print("Collecting [%s]..." % filename)
                subs.append(filename)
    # sorting vtts are important! merge vtts depends on sequence!
    subs.sort()
    # merge vtt to one single file
    combined_vtt_file = "tmp-combined-subtitle.vtt"
    # subs_str = " ".join(subs)
    # c = "cat %s > %s" % (subs_str, combined_vtt_file)
    for i, sub in enumerate(subs):
        if i == 0:
            c = "cat %s > %s" % (sub, combined_vtt_file)
        else:
            c = "tail -n +2 %s >> %s" % (sub, combined_vtt_file)
        print("\n", c, "\n")
        subprocess.check_call(c, stderr=subprocess.STDOUT, shell=True)
    print()
    # merged vtt to ass
    c = "ffmpeg -i %s %s" % (combined_vtt_file, ASS)
    print("\n", c, "\n")
    subprocess.check_call(c, stderr=subprocess.STDOUT, shell=True)
    print()
    # clean up tmp files
    for f in subs:
        if os.path.exists(f) and os.path.isfile(f):
            print("Deleting [%s]..." % f)
            r = os.remove(f)
            if r:
                print(r)
    if os.path.exists(combined_vtt_file) and os.path.isfile(combined_vtt_file):
        r = os.remove(combined_vtt_file)
        if r:
            print(r)

    # burn ass to mp4
    c = "ffmpeg -i %s -vf ass=%s %s" % (MP4, ASS, OUT_MP4)
    print("\n", c, "\n")
    subprocess.check_call(c, stderr=subprocess.STDOUT, shell=True)
    print()


if __name__ == "__main__":
    for name, arr in info.items():
        CORE = name
        SUB_URL = info[CORE][0]
        M3U8_URL = info[CORE][1]

        MP4 = "".join(["raw_", CORE, ".mp4"])
        ASS = "".join(["ass_", CORE, ".ass"])
        SUB_FILE_NAME_PATTERN = "sub-%03d.vtt"
        OUT_MP4 = "".join([CORE, ".mp4"])
        do()