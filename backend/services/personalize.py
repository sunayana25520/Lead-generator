# def build_output(company, website, signals, score, category, tech):

#     if signals.get("qa") and signals.get("hiring"):
#         pain = "Scaling QA & testing team"
#         msg = "Saw you're hiring QA engineers—are you scaling testing efforts?"
#     elif signals.get("hiring"):
#         pain = "Hiring and team expansion"
#         msg = "Saw you're hiring—are you expanding your engineering team?"
#     elif signals.get("qa"):
#         pain = "Improving QA automation"
#         msg = "Noticed QA efforts—can help improve testing efficiency."
#     else:
#         pain = "General engineering improvements"
#         msg = "Would love to help improve your engineering workflows."

#     tech_list = []
#     if tech.get("frontend"):
#         tech_list.extend(tech["frontend"])
#     if tech.get("backend"):
#         tech_list.extend(tech["backend"])
#     if tech.get("cms"):
#         tech_list.extend(tech["cms"])

#     tech_summary = ", ".join(tech_list) if tech_list else "Website Review for Email Campaign"

#     return {
#         "company": company,
#         "website": website,
#         "Tech": tech_summary,
#         "Hiring": signals.get("hiring"),
#         "QA": signals.get("qa"),
#         "Product": signals.get("saas"),
#         "Pain Point": pain,
#         "Message": msg,
#         "Score": score,
#         "Status": "Not Contacted",
#         "Follow-up": ""
#     }

def build_output(
    company,
    website,
    signals,
    score,
    category,
    tech
):

    # -------------------------
    # PAIN POINT + MESSAGE
    # -------------------------
    if (
        signals.get("qa")
        and signals.get("hiring")
    ):

        pain = (
            "Scaling QA & testing team"
        )

        msg = (
            "Saw you're hiring QA engineers "
            "— are you scaling testing efforts?"
        )

    elif signals.get("hiring"):

        pain = (
            "Hiring and team expansion"
        )

        msg = (
            "Saw you're hiring — are you "
            "expanding your engineering team?"
        )

    elif signals.get("qa"):

        pain = (
            "Improving QA automation"
        )

        msg = (
            "Noticed QA efforts — can help "
            "improve testing efficiency."
        )

    elif signals.get("saas"):

        pain = (
            "Scaling product infrastructure"
        )

        msg = (
            "Noticed your SaaS/product platform "
            "— helping teams improve engineering workflows."
        )

    else:

        pain = (
            "General engineering improvements"
        )

        msg = (
            "Would love to help improve "
            "your engineering workflows."
        )

    # -------------------------
    # TECH SUMMARY
    # -------------------------
    tech_list = []

    if tech.get("frontend"):
        tech_list.extend(
            tech["frontend"]
        )

    if tech.get("backend"):
        tech_list.extend(
            tech["backend"]
        )

    if tech.get("cms"):
        tech_list.extend(
            tech["cms"]
        )

    # remove duplicates
    tech_list = list(
        dict.fromkeys(tech_list)
    )

    tech_summary = (
        ", ".join(tech_list)
        if tech_list
        else "Website Review"
    )

    # -------------------------
    # FINAL OUTPUT
    # -------------------------
    return {

        # normalized backend keys
        "company": company,

        "website": website,

        "Tech": tech_summary,

        "Hiring": signals.get(
            "hiring"
        ),

        "QA": signals.get(
            "qa"
        ),

        "Product": signals.get(
            "saas"
        ),

        "Pain Point": pain,

        "Message": msg,

        "Score": score,

        "Category": category,

        "Status": "Not Contacted",

        "Follow-up": "",

        "Notes": ""
    }