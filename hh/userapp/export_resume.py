from fpdf import FPDF
from loguru import logger


# логирование: настройки логера из библиотеки loguru
logger.add(
    "logs/debug.json",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 MB",
    compression="zip",
    serialize=True
)

@logger.catch
def export_resume(user, user_profile, user_resume, user_edu_history, user_job_history):
    pdf = FPDF()

    pdf.add_font("Sans", style="", fname="./static/fonts/DejaVuSans.ttf")
    pdf.add_font("Sans", style="B", fname="./static/fonts/DejaVuSansCondensed-Bold.ttf")
    pdf.add_font("Sans", style="I", fname="./static/fonts/DejaVuSansCondensed-Oblique.ttf")
    pdf.add_font("Sans", style="BI", fname="./static/fonts/DejaVuSansCondensed-BoldOblique.ttf")

    pdf.add_page()
    pdf.set_font('Sans', '', 16)
    pdf.core_fonts_encoding = 'utf-8'
    pdf.cell(None, None, f'{user_profile.last_name} {user_profile.first_name} {user_profile.middle_name}')
    pdf.ln(10)
    pdf.set_font('Sans', '', 8)
    pdf.cell(None, None, f'Пол: {user_profile.gender}. Дата рождения: {user_profile.birth_date.strftime("%d.%m.%Y")}')
    pdf.ln(5)
    pdf.cell(None, None, user_profile.phone_num)
    pdf.ln(5)
    pdf.cell(None, None, user.email)
    pdf.ln(20)

    pdf.image(user.avatar, x=150, y=10, w=50)

    pdf.set_font('Sans', '', 14)
    pdf.cell(None, None, 'Желаемая должность, ЗП, режим работы')
    pdf.ln(10)
    pdf.set_font('Sans', '', 8)
    pdf.cell(None, None, user_resume.position_name)
    pdf.ln(5)
    pdf.cell(None, None, str(user_resume.min_salary))
    pdf.ln(5)
    pdf.cell(None, None, user_resume.work_mode)
    pdf.ln(10)
    pdf.set_font('Sans', '', 14)
    pdf.cell(None, None, 'Опыт работы')
    pdf.ln(10)
    for item in user_job_history:
        pdf.set_font('Sans', '', 8)
        if item.end_date:
            pdf.multi_cell(40, None, f'{item.start_date.strftime("%d.%m.%Y")} - {item.end_date.strftime("%d.%m.%Y")}')
        else:
            pdf.multi_cell(40, None, f'{item.start_date.strftime("%d.%m.%Y")} - по настоящее время')
        pdf.cell(150, None, item.company_name)
        pdf.ln(5)
        pdf.set_font('Sans', '', 8)
        pdf.cell(40, None, '')
        pdf.cell(150, None, item.position)
        pdf.ln(5)
        pdf.cell(40, None, '')
        pdf.multi_cell(150, None, item.progress)
        pdf.ln(10)

    pdf.set_font('Sans', '', 14)
    pdf.cell(None, None, 'Образование')
    pdf.ln(10)
    pdf.set_font('Sans', '', 8)
    for item in user_edu_history:
        pdf.set_font('Sans', '', 8)
        pdf.cell(40, None, str(item.end_date.strftime("%Y")))
        pdf.cell(150, None, item.edu_org_name)
        pdf.ln(5)
        pdf.set_font('Sans', '', 8)
        pdf.cell(40, None, '')
        pdf.cell(150, None, item.edu_type)
        pdf.ln(5)
        if item.course_name:
            pdf.set_font('Sans', '', 8)
            pdf.cell(40, None, '')
            pdf.cell(150, None, item.course_name)
            pdf.ln(5)
        if item.skills:
            pdf.set_font('Sans', '', 8)
            pdf.cell(40, None, '')
            pdf.cell(150, None, item.skills)
            pdf.ln(5)
        if item.comments:
            pdf.set_font('Sans', '', 8)
            pdf.cell(40, None, '')
            pdf.cell(150, None, item.comments)
        pdf.ln(10)

    pdf.set_font('Sans', '', 14)
    pdf.cell(None, None, 'Ключевые навыки')
    pdf.set_font('Sans', '', 8)
    pdf.ln()
    if user_profile.hard_skills:
        pdf.multi_cell(190, None, user_profile.hard_skills)
        pdf.ln()

    if user_profile.soft_skills:
        pdf.multi_cell(190, None, user_profile.soft_skills)
        pdf.ln()

    if user_profile.comments:
        pdf.ln(10)
        pdf.set_font('Sans', '', 14)
        pdf.cell(None, None, 'Дополнительная информация')
        pdf.set_font('Sans', '', 8)
        pdf.ln()
        pdf.multi_cell(190, None, user_profile.comments)
        pdf.ln()

    pdf.output('resume.pdf')
