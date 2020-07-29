#!/usr/bin/env python3

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
    # "8.1_OS_Scheduler_Mechanics": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_xp5f126s/segmentDuration/300/ks/djJ8MTkyNjA4MXwUQRn_UCrAuzUa6HaGLYSiOA07MHghs2zJ-b-L3KmACM1Zhrs2qa9WzO-a0kAxjYM5_dc85umlbFvv0HMcBfRYTZ9SO7zJoQDvyLGM57KxrpywwM9Q22_YoxvUym9mW1BxV4rXPgfIWyzS21olINjP_jWkh71qVkfO78ao4Ddv1sbekqHK90tp31Ia6WmgdIgR8hM47WjQsHViGzOTxCyRhiT1IIeTIgEIjg3tm6IC3cIBJZRUaGqjKFgDMCuGjDqvJsf7UlwBmI4wI_plzrQI/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_3til4cfw/v/12/ev/21/flavorId/0_49nkh1ym/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wXzN0aWw0Y2Z3L3YvMTIvZXYvMjEqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk2MDc5MjU2fX19XX0_&Signature=H-dlROAU4KoTwBbmhQr0K4c7EBBhJbPxmsFb1OP9BUUqpEFVxRMLrA7suB3LDlQTC4Z4VPSbgNPXLN0JufoYtGvFMtJQsbdKnNWJcjrtXdGI6MhWTrcehLuen2JvbYTeJ1I8rFbKc7NFy6aEGbuQ07gODuikzkMAN4PAZ0ez6tL8LiJ6K-JDwoFV9AddcGIViFNUuU9-qHcL7TmSMK8MVc0yRs06FZJjqnJDk8a0rK8iWMfznJBbBeaTTagVHiJlQN-kwf~QfI5ilTJ5Av~BXBPyfckOa1ByDQNcFdBv3fsjYtdfJ7P8zr6zrQnszbGcXaX~LnYdvU5D2KJDG8i0Rw__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "8.2_Go_Scheduler_Mechanics": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_emayv3vs/segmentDuration/300/ks/djJ8MTkyNjA4MXxoB1MW9ydbboRHgeho10ul-pu14tS4P7OFVthL6mjHTqRL2iB_8iz3o39vI5DCHm81HQyq9m_8WHeWzat0ZRCJ9mTRmGOLhH-770ffIF4YPsXR6aIpZuF5ECaCTjvRsiA7jKGV1HH0GUM2VWt-oU4lPA-TreplET24fkUGvN2cvRPOgknQnYaYXqgGCkbDinma927aZcpvu54D6elVVZ7ae8GfinX9DJMX7NL9vWtotWfgl6EIXvrQiCvaHfEjVT3lfg0zR3MGVnRDtDcxvdPj/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_g4irrhpg/v/12/ev/21/flavorId/0_m2bc7i26/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX2c0aXJyaHBnL3YvMTIvZXYvMjEqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk2MDc5NzU4fX19XX0_&Signature=EvwWWQVEXctASHm13oZ0SXyTh0h~wBpf7-Qq8V7n9D7XB8Uu7KkY~oTtC~51ygLOv0sR2MRf5KB2eMGuF-aaHCAeOYNXuc6qGZETxpZ79B~PCzW4DyHuoRieriuRS7e3wngUeTqjbxDINo3SDtkhQEghUwTst~MPBS76iGFTFL81u5gJPJFrnisnbYrsSjcx5IVbjdloyKDWrjZUroRCOk2aNZVlF12GDyMSS905VxrrU6uyxZf6p3oVHbhemtYM1I9axHR1~rHKeq6QVGThm7MCTs7~dH4v~TcRp5E0aJ28wEIRFjurPPp-kgitrR-KiFsAeUl2QTh3xtMvbb3fdQ__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "8.3_Creating_Goroutines": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_ohvg4kkb/segmentDuration/300/ks/djJ8MTkyNjA4MXwk0h4lf4G4MpM20yHLvUEElxmLvElyFxY8N-n-UXkmBV8Owwbj_HG7SgoYeKXnmlr5LM9-_5OfAAYoomzVHhg5ApqYuCU_yk4aS2ifaNc1Yz57tCSE6IZmdiM8OJZQHo54tS6CVARWX2wGPfxApJBVxNJycyEUdnv9qWuRjTE0uDgYDRN1OkvDMxZSpkPTqGFN5Fm63b1ui0lMfFB1Q6nwzNzCMBu3mm9Ce-glBY2WLTGWmnX2Z2V6TYhosV4QmaxoqNh4GHiWwqrjltWM4Sb1/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_lb09p4fp/v/12/ev/21/flavorId/0_f49vahjv/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX2xiMDlwNGZwL3YvMTIvZXYvMjEqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk2MDgxMjEyfX19XX0_&Signature=RAhpmYplubOSkMDQaRToiQlwUG0CMoC-cw8I-gMBye9cDqnUtsBKoQoelNVOqbSIHI~NhpolM7DF6qgp2gUB4QQ9Vn0oL0~BMylUmDbVclrcUqibnfjAstNhlU7J1g9O4jCjL3P~Pr9Su22XpJSl7F5BkaMfcJT-cqctpcRqBpw2WkSHConpBPbaeLhaGF~PuBPMfSpMF2thF0Sb08XcfHKo33ymm8aSlV9fcyQghUTHy01617VMJHAD9FgP0l7fAxmj39OSRhsZKAwPuaiq6ltR-Fw78rbNZMqzWcS1E-K3fefqFFkg~gQqk80ecB6rRUYobB~skhSzWmhWJTjUhg__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "14.1_Profiling_Guidelines": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_b1axvx9k/segmentDuration/300/ks/djJ8MTkyNjA4MXwXcanfelB7SPBSdNkMNwD8xaqlb96fiJHblpaIzCr0r4KRNutV6WfusmvZsOS2kgBVxSH7y6re-zdccwrmqlWizHLslpWlLZxX33eR7ofGE3kp70eY738mdq4WuPWdBNpjNoqosjSKWXPZLgAI4ULs8yzU-FVBeQ5OHkMxaOW_THZxU-ia953VkbX1lqiOTSXokyuzyw9pNsKKkKH5FvoaSn-p_f3AWBp-W6etHfgVrCTrGPvkEKZWH9HToQzSJZK14hmXj0uMgPsPCA7flORX/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_ahxemgyl/v/12/ev/21/flavorId/0_olycx298/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX2FoeGVtZ3lsL3YvMTIvZXYvMjEqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk2MDgxNzkyfX19XX0_&Signature=NIk0dYsUQook4ryq~PyXw4vAoSZ5HFj8cyWwG~LfpOyHL14ECrL9sS0ZLJK1DWp123W5HYcM0laZIZovAAnvaTbVX5MPBKC6EVM1txyLzbUS5uXIAhvnlF~2ym9fb1mygaP7RA7q-ONzOprh3AWfW3F-Yktg9Y4eD1d3sQJyIAJSosYDBRM2j57JYQxfWfnevVoKOsAfBkj47VTFE9Ry23Mroh1YVG2KRvOybCmJE7NN1muRgCubaEhWxGp6d5OJXb6OWCZpwdUzg3dh-gtK1X-SLr6tyS7rXdYtnMYTs2Nff012VyTiqdS6-8CgWbUBTgmDYgtQdewK-AUc4EN2iw__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "14.2_tack_Traces": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_8pye1rhk/segmentDuration/300/ks/djJ8MTkyNjA4MXxIFffRJMzaayRn4dYY4LaWJkQ6lwCMi0Rk5R9MWYAHKfbH72Q4Kqp5bkf_1-4AE_lhtkKw5zYmwJcc2iUO0_3pdk51z1Z5o0xzRIcJtZzZ2uJrovWyXsdt0Wmxjfj9aifU9MjX6kQbqfFoh4wx6GhwbDbEPFLbtmFNDWL4U_p6KpTOKf-al1fqUhdjkjqGyMYwmUonT5c8P7a9b3AMNUqJIcKy_QwtEJvbEgwRtTrhsTNegTQS8gYafxrdNxsrFLoRMpqIxUi6hISyxhfNx6eu/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_8dacbyrc/v/2/ev/14/flavorId/0_gwe6dnh2/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wXzhkYWNieXJjL3YvMi9ldi8xNCoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE1OTYwODMwODJ9fX1dfQ__&Signature=ZhtdhyrMm82rKRGGmBpNhcZLFIUSy2QsB9HyOv9mfLBs4EAyspWW2ACpDatcw-llU~vf20h37lAR-R9p3dJpZUB7Vj55~-yXtUw8OR5k-cLTkb~Z1nT8Yu2s-qbLEZsB7~MwIPbe7dDqBz-T9C9z0jiM1y8WiC6YVCPrpEPrFK0W~8ZX57GzuYa-mhNWMpeM9Etg8wE5C98B-fGiFzZa7yDmJ83sf2PCmA9tj-F5RB6ysVsY51~dIxweCxrIxreu8qwackaFiw3W6qTlHulUX1oZvmWDjkvCFf5DFehnxxjuG~zCGTd-qaKmrb1hLiWBaDF6Ec8dNPN-ClfbwlM-~A__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "14.3_Micro_Level_Optimization": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_xo5l0ogq/segmentDuration/300/ks/djJ8MTkyNjA4MXzizr3MAiRpXAU-D_7CT57MxKKWjHvqWo8pEyQU0k-1dPmyXNXeNdSh5AYY6agUvpLdA4-wguegX7m-k_0PmpjMnEp9oezFXvjQxUpMbcn1P96lXk37Vr3nBUeVKrrY23PI_xyZOZfZJpLu9PE8_2uSc5hoEM9G9Tlqd6kTWoCtrLIJCww5FOKnbSQOu6UzcLnPyoSscLd52i_7M7VZhP7s1FROrO-KKFPnsxfnBGOktLQrlXO-vXAcbG3XbZjUWlPZJ0kIYMgVwUW9u31jVxlo/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_7f5oiul1/v/12/ev/21/flavorId/0_oetwlya4/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wXzdmNW9pdWwxL3YvMTIvZXYvMjEqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk2MDgzMjI1fX19XX0_&Signature=E9UhHZ3uAvtH63Ob-WtEGswNey2Nm9e6LaNBJnNgJtxbao3mpX14LgQO36EjREnB~PcyNrkNV2c1jC8QoLCORTSASeBhGl6JeqmApkyDRIF0adV7tHC0O~6uEcShBJa11uAnztUHlnwyQpiaAClfBh4qlT5kZlm~tjiOMKcgzbU9TODKlISSScH8Q6v1J-Rd2brOewnq~o~xUCH-Meh~DKl1dnX4U5UnxMVBWkGs-R22kCxi98mzVJ1lAeiwaPJQS6E1ItUr3hEuJSCgfoyGDSEo1eg~YduTzXXcIjbvhLZlBw5MwdjVV8P~hgj~YS-c1U3NgcSoDAOyLwtGYuY38w__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "14.4_Part_1_Macro_Level_Optimization_GODEBUG_Tracing": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_p2dtz45v/segmentDuration/300/ks/djJ8MTkyNjA4MXz_QOQQFXzcOT2zeP75A9tvBeCkGBvbQZH9FlNgLTBigNk45b8taqzeGvJyfmwXQmEonqCdT_Cvfnwgm3J3XRHDHfYyNWFJfilRovCvhMOv46axjLdyf98T8y5VjpZuNe2AEqI1xXGUikNCl9OtvBe1sVmeGuiGUeTitwEN_4cGEzAVuWRO3GyzCieEjY6hUmk3CPQPjpX7gOt5AQlrr5XNUz4lX0xTiSw46b8rt9igAdsUzbloFfx9V03Bm1fMLGZB8x6CmDosE4o3OymyokWJ/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_ge8fyna6/v/12/ev/21/flavorId/0_foyoqqjh/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX2dlOGZ5bmE2L3YvMTIvZXYvMjEqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk2MDgzMzYzfX19XX0_&Signature=LcQuG4f7AttiwMdAhVdEEob1ip~j8OedMOht4tpMQ-j09A5485YmawifUkzrdMjPJYlpuGiE8c7Dcbb-lgfhKnY2BQui2B8X9uoexoafdvqXHwBB~w6bxBMhoTXHBsBCOo2VJhgyAI6TjZbjnCcw4cQ6N9ewPXMUraA8Pv8idqmBr8jQug7EqXOpYVCkKZVPUfn2JV61rHzuVk6pyFCcAJtostTEfHRgGRvp6mmm-RNLbtzFJO3CbRyn8YTh-ycGObna~war8X6lQaK-ilqR~abc1O~-u5zWd7C15zzk3jM8syOr2I9N45zQdM0pZL5zANAjRbO2vnEf05~ctImCYA__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "14.4_Part_2_Macro_Level_Optimization_Memory_Profiing":["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_hu3vtuno/segmentDuration/300/ks/djJ8MTkyNjA4MXykESyPxSIkjqL8gDk9WtQtizcOSxYpwVL-Nh1hN5Rf5flgCcYexB5SgVaGGOM_7eHDDjfzl9-Zd-jjrx59A-l_F_iP9vMeeLBYvX2Yky-M9XBVho-BuTA090K72K789gtrQclESUphzIsDzxHx3Bm_gbbFLEDpgIsQm7yN31LufKYe7fJehNrM-6kRjwImPpbyyc5qOxy6m2YiozJvIFp-OmGgX9bW6OeIy8MYO3db1SuXkZuczs8ipV2JyFb84H-lupVDl-WCPpkrvNeI74mv/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_r9gx765m/v/12/ev/21/flavorId/0_4iq9v4v6/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX3I5Z3g3NjVtL3YvMTIvZXYvMjEqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk2MDgzNDc4fX19XX0_&Signature=aUhWDXjp9Rgo7ChMhVj~dpDKSmU5sT5HvboqGKC1oBBbv3~cGgA-kxSwdM6h1KraX99vf4KHaD5fSYVIHkpagK~OtZMGvUFQq9bNmhk9lKk0Myu4VFhKqg-As93VDFyvpIq~hNnKJJ-ji97m21bcanqN9AmyQ8N6jht6Ec6NQGFoN89xQNtnmmBQVQdp6npfag6bZi0Uoa112YlrfBaxhdt2PZN188JQeh5llGCmYPU9S5yUYO8R0wY4O1gH0B3t4OJTptigQYNAdwPW5ujVCfkksHSegwiHZo4PyDFP2oVeQONtn1ei6L3JSalKBE-53uCJUb74apgsKatAFxY4gg__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "14.4_Part_3_Macro_Level_Optimization_Tooling_Changes": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_hkzf82v6/segmentDuration/300/ks/djJ8MTkyNjA4MXw6j8VuXtvFTW8Nwc7pNdlg01NpIsL7EwV_3wRdqviDcx5e6tpDeVDI9R8CcliXh92Ln4FS2PhbRGnLsFWqV1MMBcAbQ8qqmJSMvlhCOJuLbrYa0Sg9aLcz3YyATwqLwVLMOBYwL3m64jifsG1_evU45vyUnqKSnclaeDS1M-T7vx36LmhWVZYXXbT_OsYyViVp55rohqKuTGpiUYYB7oqEuLFQXUfXrY5poxJtEwCUJSKxpvUzn2IZYoT4HhFe3iXLGCqY_hzTOL8JF9ytLdRt/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_f2s3izjt/v/12/ev/21/flavorId/0_tblscdhh/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX2YyczNpemp0L3YvMTIvZXYvMjEqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk2MDgzNjQwfX19XX0_&Signature=F8tbPcVJZ1B7LTzmRF7ycvO7tT7Olc2zrfiLQpyDOiwOFptoMGgGiiHCS5Ttf98agXC79ig~B-fJv5g6UKjng--TMj5x~F6JIT0hCdROtQTyvGKHyLaF~BnSO85yD6zGWCzTpt7I8m3HPlR4UmXK2RPt2AFoFQKqDFcE1EVBEpJPSBQaMLANakwC5IoTUQCEYpAemBRZ4CAhaJMuudFJIzDOgWDweoiz9oJ3qpYwgL99u7B1yNwvQdeAE5AHIu1yx1vjVafhmBZSLfLcpMg9TWdquAb6yfX-Uujc7DeJZjQU-nUYAasvdzWqgy29Pi5MPANp4gTbarTYg7IfD~Vqtw__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "14.4_Part_4_Macro_Level_Optimization_CPU_Profiling": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_ytvf45hu/segmentDuration/300/ks/djJ8MTkyNjA4MXw5pYen46ExpvPKZ3HPgqHpbjypyVsahY8kYX9NfieINHoTrAHVFUsHyq9u1tLFbmRn5nTzkV1-g3z-4TbAmIFHjCsqelaW8XX8uIS92suw2Dx3i5m1qh4f0jr8eQiQmJu7vOPZfKV4d_uiBhidsoDUuZ_L42AOypV-jWwyZzPU3pFDAEJu3-qsPi4gyax0fMyGMdDuWR_Zg8hsznvHUVK2rGHT63hP6sV-wknBd54Q3n0IdO_-f_xn_80HpinH7_7GSepiGxj_6dGtQtwWsfjl/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_woraaxtp/v/12/ev/21/flavorId/0_ey1hv4bw/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX3dvcmFheHRwL3YvMTIvZXYvMjEqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk2MDgzNzQ3fX19XX0_&Signature=cPFPAhjdzJEmpro52lt4GlfsP~0mMZDnA6ZQnK-WcQoZS2rDWbRKpH2klGDcGSlzxlYLETm7KW4fKwur2IweBaTzLtQF5n8YGnfFK~xdVnCpHdwFR-GGU3reKdWVFFb9syVD~iAnJCNC05N3yZPVbrb5T6eewx9OSZSxJKnKf5-gviXVZZb8oDvIQ-ju8HEYEmM1hL3idlUdO9tOD1retuldOFgajLPjCCAb2WZ4Ca0hF6z5CNA5bcuP6BOXepatoxiaL~iDB2GYDqVrXWzJHtw0-aKj4QZqgLR5M9LhOKX7u1VkNuTzYEVWc7WzqIY5jlnnEj8d5Hsj8c1jnFV9vA__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "14.5_Execution_Tracing": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_kpbd0in9/segmentDuration/300/ks/djJ8MTkyNjA4MXzVUsZvHVMp33HgPmhP3Vr6dIVoAOJ_8-LLW81rTN8l2yr36deblRGGU1i0kTFKJtluYO5_LnDr3OiCKsD71rx8X1Bp_MGQOubFzEs00cBHkwPsErQ9u_EShJkhCm4BQbR5pFRk7FzlbB_yeFhHA6dj7JIWV_BXOQbcAskJP49Q8WMFTBsPZHxgW-__TzK7jGV9pQzSm_ICIUxFnAkePT5lhQyu0bvU398VQi-cMoKETDUIhsKR8VMvpGhc0ciG0s_ml7AI3gJ7et0Mx0i_Tcab/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_fg8wdwoo/v/12/ev/21/flavorId/0_mulvipsv/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX2ZnOHdkd29vL3YvMTIvZXYvMjEqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk2MDgzODM1fX19XX0_&Signature=Wf7aLX1m~GIrQiZME4n3cw9w7buiEfoAC3SgARcqaSvY-V--4qXv31wflJ3SolsXAm4m-RrBrQXdz7qpR8at6KCoY9XTVN837CCKN187vItS8sQVUna81a5p4cnDaYGVFskxl-DMCaHUpY6MYnfToRMvugSHRixUqhXvWLh2eEUJcYVXi6FRVAn1RX2FQ~9ml~cbaQsElvYcwIwecNH69eKHMltiTJAcY2LUrlNyGm03KVosFfWbOCJAL5L8AStXZrZmrF8epKqgVDujc1Cx-W5BqTSLgTOYYDq8kQ2WMbbJlv8~tTOnuSWtcbBfAwyRMkShvFK6YuEc2njLQsuzzw__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
    # "14.4_P2_Macro_Level_Optimization_Memory_Profiing": ["https://cfvod.kaltura.com/api_v3/index.php/service/caption_captionasset/action/serveWebVTT/captionAssetId/0_hu3vtuno/segmentDuration/300/ks/djJ8MTkyNjA4MXyDA8aFq9LDRUOS2bdKolQxDbrdYDD0vWkiOCchVZoqKJ3n4qOVOdnn1aMiGD6Dg8BSE3wyTJnFylVewUx3QRgO7ENmTGdFF5l4lG_d7p47n89X8NdMrlEAoBqy4A0amfHT128MP8woLqcAOsby_nremB73ZyX-ZGoV2YmBYAOl-Hkl2_upksxb4kzADZCdhfNazKZtrPcvsD9C0ZWZHIMWaQQH8JsQjQd3_qZzEL7uCWkD_F3p4cFiu6D_sFKcN7zHa1cYrGCo2iHGsl9ujv72/version/72/a.m3u8", "https://cfvod.kaltura.com/scf/hls/p/1926081/sp/192608100/serveFlavor/entryId/0_r9gx765m/v/12/ev/21/flavorId/0_4iq9v4v6/name/a.mp4/index.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTkyNjA4MS9zcC8xOTI2MDgxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX3I5Z3g3NjVtL3YvMTIvZXYvMjEqIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk2MDM2NjUzfX19XX0_&Signature=HfGfKmpNqHb6GQ1Kcy7Jauvz9c3SsMaouhUwZBC9GB6wDFpYa8bePmEhvMUwx1gPTh5HGLh~tzzYhLmZSXRHDxH~01tAp8nbKWn00JAai6ghL02AtyFCnf59pUX-XcQPhWKr~GlfYwqu-JpI8mnrV~Pa3bBs89qHliE7YsWltVJHHfwwXnavr5Vx5jOSD~UIyRyGi-Jr5d5cDq5r~PBML56dRgTy7BUz0NR5bLWCgcCb93hUTYVy5oD79s2JpTHAUes9pCTxWzd7YmOHkhhSO5fS2YjhhwC3-ZomBn0TwLTuLGozbXF41496BEooczU1lwbg5tYfbmtx79jnD50bxw__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"],
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