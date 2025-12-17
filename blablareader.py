from playwright.sync_api import sync_playwright, expect
from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError
import re

nikke_dict = {
    511 : "Cinderella",
    352 : "Helm",
    162 : "Mihara (Bondage)",
    191 : "Alice",
    15 : "Anis (Summer)",
    183 : "Maiden (Ice)",
    514 : "Grave",
    16 : "Rapi (Red Hood)",
    850 : "Eve",
    851 : "Raven",
    225 : "Scarlet (Black Shadow)",
    835 : "Asuka (WILLE)",
    513 : "Little Mermaid",
    234 : "Dorothy (Serendipity)",
    194 : "Ludmilla (Winter Owner)",
    502 : "Elegg (Boom and Shock)",
    450 : "Naga",
    330 : "Crown",
    82 : "Liter",
    355 : "Anchor (Innocent Maid)",
    354 : "Mast (Romantic Maid)",
    353 : "Helm (Aquamarine)",
    32 : "Miranda",
    832 : "Mari",
    272 : "Rouge",
    143 : "Milk (Blooming Bunny)",
    315 : "Ade (Agent Bunny)",
    223 : "Nayuta",
    830 : "Asuka",
    262 : "Liberalio",
    75 : "Diesel (Winter Sweets)"
}

user_dict = {
    "MjkwODAtMzg0MjE0MDEzMTk1NTQ1NzY5Mw" : "Moar",
    "MjkwODAtOTI4MDU0NjgyMzY2ODE4MzA5Mg" : "Silkee",
    "MjkwODAtMTU2NDY1MjQyNDIzMjc1NDk4Mzg" : "CRANE",
    "MjkwODAtODQ1MzAzOTMyMjczMDM1MTQzOA" : "Marin",
    "MjkwODAtMTQ1MTg3NDY4MDIxODMxNjYxMDc" : "BEHXBEH",
    "MjkwODAtMTY3MjMyNjk2MDA0OTUyNjAyODE" : "MAXBLUE",
    "MjkwODAtMjU0ODM0NTA2MDEwMzI2MjA2MQ" : "VELLIS",
    "MjkwODAtMTkxNDQwNDczNDM2NDgyNzY5" : "STROOKY",
    "MjkwODAtNDM2MTQzOTk2MzA1MDM4NTMzMg" : "AMEBLANC",
    "MjkwODAtMjIxMjQ5MjIzNzY4NzA4MTM5MQ" : "PAPER",
    "MjkwODAtMTA5Nzk2NTIyODUyODc2MTA1NDE" : "NOELBEAR",
    "MjkwODAtMTYxOTcwNjY4OTI4MTM4MzAyMzI" : "GUN",
    "MjkwODAtMzM3MzA4NDc4MTYwMTAyNjc3OQ" : "RANDOM",
    "MjkwODAtMTE5NTYzODU3MDkyMzExMTA0Mw" : "HATCH",
    "MjkwODAtMjg0NjYwNzU1OTg3MTYyNTQ5Nw" : "VESAGO",
    "MjkwODAtOTcxMDk0MTcyODY4OTU4OTQ1OQ" : "AME",
    "MjkwODAtODk4NDk4Mjc2MTcxNjg2ODMxNA" : "LE0N",
    "MjkwODAtMTM1OTA2NzM4NzY1NDI5OTQ1MjE" : "BEHXBEH2",
    "MjkwODAtOTAyNjc4MjE4ODUzNTgxMzEyNw" : "BCP",
    "MjkwODAtMTAyMDk3MDEyODk5NDEwNjI1OTk" : "MONO",
    "MjkwODAtMzg3MDU4NTYzNDE3ODU1Mjk4NQ" : "Eldloup",
    "MjkwODAtMTE5NDI0ODQyNjg4NzI2MTI3Mzk" : "Vaylin",
    "MjkwODAtNTMxOTc4MzYwNjE2ODU0NzA5Ng" : "BCP2",
    "MjkwODAtMTIxMjY1ODQ3MzI0MDAxNTMwMDM" : "Luxury",
    "MjkwODAtMTgyNzA4NTYyMTg4MzM0MjE5OTQ" : "Joseph",
    "MjkwODAtNjI0NjAxNzkxMTIwNzA4OTEyOQ" : "Margulis",
    "MjkwODAtODMyNDg5NDI1ODE0NDQ5NDMwNQ" : "Gungnir",
    "MjkwODAtNDUxOTQ1MjY2NzIxOTY2MDkxNA" : "Fenniken",
    "MjkwODAtNTYyMTI3MDQ2MjI0NjIxNTEyOQ" : "Yor",
    
}

def login(page):
    ######  LOGIN
    #This breaks sometimes so if you keep getting owned comment out everything after the expect and before the input#
    page.goto('https://www.blablalink.com/login')
    expect(page.get_by_text("HK/MC/TW")).to_be_visible()
    page.get_by_text("Reject all optional cookies").click()#
    #page.get_by_text("HK/MC/TW").click()#
    #page.get_by_text("HK/MC/TW").click()#
    #page.get_by_text("JP/KR/NA/SEA/Global").click()#
    input("Please login and complete the CAPTCHA in the browser. Press Enter here to continue once you are finished logging in.")

def scrape_nikke_details(page, link):
    page.goto(link)
    expect(page.get_by_text("You can use materials to upgrade NIKKEs")).to_be_visible(timeout=15000)
    # try:
        # locator = page.get_by_text("Equipment Effects", exact=True)
        # locator.wait_for(state="visible", timeout=5000)
        # parent = locator.locator("..")
        # grandparent = parent.locator("..")
        # print(grandparent.text_content())
        # return grandparent.text_content()
    # except PlaywrightTimeoutError:
        # print("'Equipment Effects' not found after 5 seconds, skipping.")
        # return "missing"
        #Check equipment
    equipment_str = ""
    try:
        locator = page.get_by_text("Equipment Effects", exact=True)
        locator.wait_for(state="visible", timeout=5000)
        parent = locator.locator("..")
        grandparent = parent.locator("..")
        equipment_str = grandparent.text_content()
    except PlaywrightTimeoutError:
        print("'Equipment Effects' not found after 5 seconds, skipping for " + link)
    #Check skills
    skill_str = ""
    lvl_str = ""
    try:
        #Check Level
        visible_text = page.locator("body").inner_text() 
        lvl_str = str(re.findall(r"LV\d{3}", visible_text))
        #Check Skills
        page.get_by_text("Skill", exact=True).first.click()
        max_links = page.get_by_role("link", name="max")
        for i in range(max_links.count()):
            max_link = max_links.nth(i)
            skill_container = max_link.locator("..").locator("..")
            text = skill_container.text_content().strip()
            ntext = text.split("min-1+1max")[0]
            skillnum = ntext[-1:]
            if skillnum == "0":
                skillnum = "10"
            skill_str += (f"|Skill {i+1}: {skillnum}")
    except PlaywrightTimeoutError:
        print("Timeout occured during level or skill matching for: " + link)
    #Check doll lvl and rarity
    doll_rarity = ""
    doll_phase = ""
    try:
        page.get_by_text("Collection", exact=True).first.click()
        rarity_locator = page.locator("text=/^(R|SR|SSR)$/")
        rarity_locator.wait_for(state="visible", timeout=3000)
        rarity = rarity_locator.inner_text()
        if rarity == "R":
            doll_rarity = "|R|"
        elif rarity == "SR":
            doll_rarity = "|SR|"
        elif rarity == "SSR":
            doll_rarity = "|SSR|"
        else:
            print("error: rarity")
        phase_locator = page.locator(r"text=/^Phase (?:[0-9]|1[0-5])$/")
        doll_phase = phase_locator.inner_text().strip()
    except PlaywrightTimeoutError:
        print("Timeout occured during collection matching for: " + link)
        
    ret_str = equipment_str + skill_str + doll_rarity + doll_phase + lvl_str 
    print(ret_str)
    return ret_str
    

if __name__ == "__main__":
    #Don't delete the data.txt file for now but will probably replace this with a much better way of storing data (probably csv)
    with open("data.txt", "a", encoding="utf-8") as f:
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=False)  # Set headless=True to run silently
            page = browser.new_page()
            #LOGIN
            login(page)
            #  CHECK PAGE
            for uid in user_dict:
                for nikke_id in nikke_dict:
                    link = f'https://www.blablalink.com/shiftyspad/nikke?nikke={nikke_id}&uid={uid}'
                    f.write(user_dict[uid] + " " + nikke_dict[nikke_id] + " " + scrape_nikke_details(page, link) + "\n")
                body_text = page.content()
            input("Done! Press enter to save the data to data.txt")