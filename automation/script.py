from pandas import DataFrame
import asyncio
from xmlrpc.client import ServerProxy
from playwright.async_api import async_playwright as playwright
from base64 import b64decode
import logging
import sys
from os import makedirs
from os.path import dirname
from dotenv import load_dotenv
import os

# Carga variables de entorno
load_dotenv()
ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

BASE_URL = os.getenv("PLAYWRIGHT_BASE_URL")
ATTACHMENTS_PATH = os.getenv("ATTACHMENTS_PATH")
FORM_USERNAME = os.getenv("FORM_USERNAME")
FORM_PASSWORD = os.getenv("FORM_PASSWORD")

# Configura logging: fichero + stdout
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# FileHandler
file_handler = logging.FileHandler('registro_fronteras.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# StreamHandler (stdout)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


async def login_crm():
    """
    Connects to Odoo CRM and retrieves employee records.
    """
    try:
        common = ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})

        logger.info(f"Successfully connected to Odoo. UID: {uid}")

        models = ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
        employees = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'hr.employee', 'search_read',
            [[]],
            {
                'fields': [
                    'name', 'work_email', 'department_id',
                    'coach_id', 'job_title', 'phone'
                ],
                'limit': 5
            }
        )

        logger.info(f"Retrieved {len(employees)} employee records.")
        return ODOO_DB, uid, ODOO_PASSWORD, employees, models

    except Exception as e:
        logger.error(f"Error connecting to Odoo: {e}")
        raise


async def get_attachments(models, db, uid, password, employee_id):
    """
    Retrieves attachments for a specific employee.
    """
    try:
        attachments = models.execute_kw(
            db, uid, password,
            'ir.attachment', 'search_read',
            [[
                ['res_model', '=', 'hr.employee'],
                ['res_id', '=', employee_id]
            ]],
            {'fields': ['name', 'datas', 'mimetype']}
        )
        return attachments
    except Exception as e:
        logger.error(f"Error retrieving attachments for employee {employee_id}: {e}")
        return []


def save_attachment(attachment_data, filename):
    """
    Decodes and saves the base64-encoded attachment to the local filesystem.
    """
    makedirs(dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(b64decode(attachment_data))


async def sent_information():
    """
    Main function: retrieves employees and attachments from Odoo,
    then submits data to a local web form using Playwright.
    """
    try:
        db, uid, password, employees, models = await login_crm()
        df = DataFrame(employees)

        df['department_name'] = df['department_id'].apply(
            lambda x: x[1] if isinstance(x, list) else None
        )
        df['coach_name'] = df['coach_id'].apply(
            lambda x: x[1] if isinstance(x, list) else None
        )
        df.drop(['department_id', 'coach_id'], axis=1, inplace=True)

        async with playwright() as p:
            browser = await p.chromium.launch(headless=True, slow_mo=1000)
            page = await browser.new_page()

            for _, row in df.iterrows():
                attachments = await get_attachments(models, db, uid, password, row['id'])

                await page.goto(BASE_URL)
                await page.wait_for_load_state('networkidle')
                await page.wait_for_selector('input[name="username"]', timeout=20000)

                await page.fill('input[name="username"]', FORM_USERNAME)
                await page.fill('input[name="password"]', FORM_PASSWORD)
                await page.click('button[type="submit"]')
                await page.wait_for_url('**/registrar/')

                await page.fill('input[name="requerimiento"]', row['name'])
                await page.fill('input[name="frontera"]', row['work_email'])
                await page.fill('input[name="usuario"]', row['job_title'])
                await page.fill('input[name="equipo_medida"]', str(row['phone']))
                await page.fill('input[name="curva_tipica"]', row['department_name'])
                await page.fill('textarea[name="certificaciones"]', row['coach_name'])

                if attachments:
                    for attachment in attachments:
                        filename = f"{ATTACHMENTS_PATH}/{attachment['name']}"
                        save_attachment(attachment['datas'], filename)
                        await page.set_input_files('input[name="adjunto"]', filename)

                    logger.info(f"Registered employee with attachment: {row['name']}")
                else:
                    logger.info(f"Registered employee without attachment: {row['name']}")

                await page.click('button[type="submit"]')

    except Exception as e:
        logger.error(f"Error during registration process: {e}")
        raise


# Entry point
asyncio.run(sent_information())
