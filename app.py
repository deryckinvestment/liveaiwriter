from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Define the consultant contact details
consultant_contact_details = {
    "Tom Lipczynski": "Tom Lipczynski, Principal Associate Dental Division\nM: +61468 305 280\nE: tom@gorillajobs.com.au",
    "Jordan Casey": "Jordan Casey\nPrincipal Associate\nMental Health Division (QLD)\nM: +61 468 842 406\nE: jordan@gorillajobs.com.au\nL: https://www.linkedin.com/in/jordan-casey-a4473a234/",
    "Jimmy Bosmans": "Jimmy Bosmans, Managing Partner\nM: 0468451292\nE: jimmy@gorillajobs.com.au",
    "Hayden Kaylani": "Hayden Kaylani\nPartner & Manager\nDoctor Division\nMedical Imaging Division\nM: +61 423 739 094\nE: hayden@gorillajobs.com.au",
    "James Enderby": "James Enderby\nAssociate Partner\nDoctor Recruitment\nDivision Manager of Pharmacy & Dental Recruitment\nM: +61 468 378 285\nE: j.enderby@gorillajobs.com.au",
    "Daniel Sheining": "Daniel Sheining\nAssociate Partner\nVictoria, Tasmania, and ACT Doctor Recruitment\nM: +61 478 524 017 (preferred)\nT: 1300 627 687\nE: d.sheining@gorillajobs.com.au",
    "Declan Lindsay": "Declan Lindsay\nPrincipal Associate, Pharmacy Division\nM: +61 468 809 629\nE: declan@gorillajobs.com.au",
    "Rosalie Hoek": "Rosalie Hoek\nAssociate, Pharmacy Division\nM: +61 478 765 544\nE: rosalie@gorillajobs.com.au",
    "Daniel Cappellacci": "Daniel Cappellacci\nHead of Legal Recruitment\nM: +61 468 718 155\nE: daniel@gorillajobs.com.au",
    "Jem Melcher": "Jem Melcher\nAllied Health Division Manager\nM: +61 468 760 842\nE: jem@gorillajobs.com.au",
    "Charlie Summers": "Charlie Summers\nDivision Manager Mental Health | Allied Health Division VIC\nM: +61 468 825 047\nE: c.summers@gorillajobs.com.au",
    "Piper Cameron": "Piper Cameron\nAssociate, Allied Health Division WA\nM: +61 468 341 546\nE: piper@gorillajobs.com.au",
    "Emma Elleson": "Emma Elleson\nAssociate Partner Allied Health Division, QLD\nM: 0468 412 394\nE: emma@gorillajobs.com.au",
    "Danny Geary": "Danny Geary\nSenior Associate, Occupational Rehabilitation Division (Australia-Wide)\nM: +61 468 314 642\nE: danny@gorillajobs.com.au"
}

openai.api_key = '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'

@app.route("/", methods=["GET", "POST"])
def index():
    advert_html = None

    if request.method == "POST":
        job_title = request.form["job_title"]
        company_overview = request.form["company_overview"]
        key_requirements = request.form["key_requirements"]
        salary = request.form["salary"]
        consultant_name = request.form["consultant_name"]
        job_location = request.form["job_location"]
        division = request.form["division"]
        selected_consultant_details = consultant_contact_details[consultant_name]

        division_outputs = {
            "Medical Imaging": """Medical Imaging Professionals inquire about:
- Working Hours: Monday to Friday? Weekend work? Flexibility in start and finish times? Flexibility in working days?
- Contracts: Permanent or locum work? Full-Time or Part-Time? Pathway for career progression?
- Type of Practice: Privately owned medical imaging provider? Corporate healthcare organization with centers across Australia?
- Onsite Services: High-end equipment (GE, Phillips, Cannon)? Exposure to range of modalities? Mixed or specialized caseload? Broad range of scanning skills needed?
- Support: Supportive management? Employee Assistance Programs? Administrative support? Generous or restricted scanning times? Paid memberships? Conference leave? Paid parental leave? CPD allowance? Salary reviews?
- Parking and Public Transport: On-site parking? Proximity to train stations and public transport hubs?
- Salary: Hourly rate? Annual salary package? CPD allowances?""",
            "Doctors": """Doctors inquire about: Working Hours (e.g., weekdays, part-time, after-hours, weekend work, on-call duties, flexibility); Contracts (e.g., flexibility, restrictions, term); Practice Type (e.g., ownership, size, establishment); Onsite Services (e.g., Allied Health, General Practice, Dental, Pharmacy); Centre Setup (e.g., modernity, renovation, purpose-built, heritage, room availability, facilities); Practice Support (e.g., nursing and administrative staff, record-keeping, appointment system); Transport (e.g., parking, proximity to public transport); Salary (e.g., percentage of billings, income guarantee); Centre Busyness (e.g., booking status, patient base growth, reputation, walk-in frequency, pace of practice); Billing Type (e.g., Bulk, Mixed, Private, patient workload, consultation fees, consultation times, approach to care); Centre Setup (e.g., room availability and quality, personal consultation room).""",
            "Allied Health": """Allied Health Professionals inquire about:
- Working Hours: Monday to Friday? Weekend work? After hours work? Negotiable working hours and days? Flexibility in start and finish times? 9-day full-time working fortnight?
- Contracts: Permanent Full-time? Part-time? Locum work? Pathway for career and leadership progression? Work From Home or Telehealth opportunities in Speech Therapy and Occupational Therapy?
- Type of Organisation: Privately owned allied health clinic? Larger allied health organization with multiple locations? Allied Health work in a multidisciplinary Medical Centre or General Practice?
- Onsite Services: Physiotherapy, Speech Therapy, Occupational Therapy, Rehabilitation, Nutrition, Mental Health, etc.? Specializations in Pediatrics, Sports Injuries, NDIS, Aged Care, Occupational Health & Safety, Return-to-Work Plans?
- Size and Setup: Large multidisciplinary team? Small clinic with administrative support? State-of-the-art facilities? Local or interstate opportunities? Individual and group therapies? Dedicated clinic rooms? Community work?
- Support: Comprehensive induction and onboarding? Family-friendly clinic? Contained travel? Supportive multidisciplinary team? Resources for work from home or telehealth? Administrative support? Supervision from senior clinicians? Professional Development allowance? Recorded Professional Development library? Team meetings? Social events? Pursuing special interests? Low KPIs and billable hours? Manageable caseload? Employee Assistance Programs? Study and Maternity leave? Internal and External Professional Development?
- Parking and Public Transport: On-site parking? Proximity to train stations and public transport hubs?
- Salary: Salary range? Performance-based bonus structure? Commission scheme? Incentive schemes? Employee benefits? Salary packaging?""",
            "Pharmacy": """Pharmacists inquire about:
- Working Hours: Flexible roster? Monday to Friday? Weekend work? Night shifts?
- Contracts: Permanent or locum work? Full-Time or Part-Time? Leadership progression? Partnership potential?
- Onsite Services: Webster packs? Patient counseling? Vaccinations? Methadone treatment?
- Size and Setup: Nearby medical centres? FRED Dispensing software? Collaborative work environment? Modern and well-equipped?
- Support: Supportive owner? Dispense Technicians? Mentorship? Training and upskilling opportunities?
- Parking and Public Transport: On-site parking? Proximity to train stations and public transport hubs?
- Salary: Hourly rate? Annual salary package? KPIs and Bonus structures? Weekend work rates? Accommodation/relocation assistance?
- Pharmacy Busyness: Foot traffic? Daily script volume? Dynamic role?
- Practice Type: Privately owned? Corporate healthcare organization? Hospital pharmacy?""",
            "Legal": """Legal Professionals inquire about:
- Working Hours: Monday to Friday? Weekend work? Flexibility in start and finish times? Hybrid working arrangements including work from home?
- Contracts: Permanent Full-time contract? Pathway for career progression?
- Size and Services: Law firm with multiple legal services or specialized law firm? Specializations in Taxation, Construction, Insurance, Families, Business & Commercial, Personal Injuries, etc.? Boutique law firm?
- Support: Mentorship and supervision from senior lawyers? Autonomy over caseloads? Collaborative office culture? Administrative and marketing support? Supportive Partners attracting top-tier work? Paralegals? Regular social events? Low turnover rate?
- Parking and Public Transport: On-site parking? Proximity to train stations and public transport hubs?
- Salary: Salary range? Performance-based bonus structure? Competitive incentive schemes?
- Firm Busyness: Solid pipeline of work? Dynamic role?""",
        }

        division_output = division_outputs.get(division, "")  # Get division-specific output

        prompt = f"""
        Create a job advertisement for the following position:

        Job Title: {job_title}
        Division: {division}

        - Provide a 155-character summary of the job.
        - Start the summary with "Our Client" and mention what they are, for example, a medical centre, a legal firm, a dental centre, an allied health provider. Sell it well and make sure to mention the job title found in {job_title} and make sure to mention the location found here {job_location}.
        - Write a 100-word to 200 word paragraph about the company, highlighting the following: {company_overview}. Avoid plagiarism and keep in mind {job_location}. Remember, this position is NEVER with us, so avoid using "we" or "us". Instead, refer to the client as "they" or "our client".
        - Provide a 150-word to 25.-word paragraph about the position relevant to {job_title} and keep in mind the location {job_location}. It's important that the applicant can envision what their job would be like and what their day-to-day activities would be. Think about what's unique about the role and how it impacts the candidate. Remember, this position is NEVER with us, so avoid using "we" or "us". Instead, refer to the client as "they" or "our client".
        - Give a 150-word paragraph about the location, focusing on selling the area and its uniqueness. It needs to be about {job_location}. Remember, this position is NEVER with us, so avoid using "we" or "us". Instead, refer to the client as "they" or "our client".
        - List 4 to 10 key benefits of the role, including the salary: 
            <ul>
                <li>{salary}</li>
                <!-- Add more bullet points here -->
            </ul>
        - Mention up to 5 key requirements for the candidate:
            <ul>
                <li>{key_requirements}</li>
                <!-- Add more bullet points here -->
            </ul>
        - Include contact details relevant to the recruitment consultant: {selected_consultant_details}

        {division_output}

        Please format the response with HTML tags in the following way:

        <h2>Job Title:</h2>
        <p>155-character summary of the job</p>
        <h2>About The Company:</h2>
        <p>100-word to 200 word paragraph about the company</p>
        <h2>About The Position:</h2>
        <p>100-word to 200 word paragraph about the position</p>
        <h2>About The Location:</h2>
        <p>1Give a 150 word paragraph about the location</p>
        <h2>Key Benefits of The Role:</h2>
        <ul>
            Bullet points (4 to 10)
        </ul>
        <h2>Key Requirements:</h2>
        <ul>
            Bullet points (maximum 5)
        </ul>
        <h2>Contact Details:</h2>
        <p>Relevant to the recruitment consultant</p>
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "- your role is to function as a recruitment consultant for Gorilla Jobs. It's crucial that you consistently refer to the client as 'our client', underlining the reasons why potential candidates should consider joining their team. Your task is to create content that vividly illustrates the role to prospective candidates, making it as clear and enticing as possible. Your writing should provide a comprehensive understanding of the job responsibilities, crafted in a persuasive manner that encourages the reader to take the next step and apply. Feel free to incorporate any additional pertinent details that could potentially attract candidates. Ensure your language adheres to Australian English standards, avoiding any slang or colloquialisms. Maintain a professional tone throughout, but avoid being overly formal and write natural avoid broken sentences or paragraphs. Your language should strike a balance between being personal and professional. Your writing should be free of any spelling or grammar errors. Avoid unnecessary repetition and over-complicated sentences to ensure clarity and readability. Remember, your primary goal is to present our client's job in the most appealing and understandable way possible.  "},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the generated text
        advert_html = response.choices[0].message.content

    return render_template("form.html", advert=advert_html, consultants=consultant_contact_details.keys())

if __name__ == "__main__":
    app.run(debug=False, port=5000)