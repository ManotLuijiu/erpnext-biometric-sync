# Biometric Attendance Sync Tool / เครื่องมือซิงค์ข้อมูลการเข้างานด้วยไบโอเมตริก (For ERPNext / สำหรับ ERPNext)

[🇬🇧 English](#english-version) | [🇹🇭 ภาษาไทย](#thai-version--ภาษาไทย)

---

## English Version

Python Scripts for retrieving data from the Biometric Attendance System _(BAS)_ and syncing with ERPNext.

### Table of Contents

- [Pre-requisites](#pre-requisites)
- [Usage](#usage)
- [Setup Specifications (For CLI)](#setup-specifications-for-cli)
  - [UNIX](#unix)
- [Setting Up Config](#setting-up-config)
- [Resources](#resources)
- [License](#license)

### Pre-requisites

- Python 3.6+

### Usage

The `erpnext_sync.py` script is the core of this project. More details can be found in [/Wiki](https://github.com/frappe/biometric-attendance-sync-tool/wiki)

### Setup Specifications (For CLI)

1. Install dependencies:

   ```bash
   cd biometric-attendance-sync-tool
     && python3 -m venv venv
     && source venv/bin/activate
     && pip install -r requirements.txt
   ```

2. Configure `local_config.py`:
   Copy the `local_config.py.template` file and rename it. More details at [Setting Up Config](#setting-up-config)
3. Run the script using `python3 erpnext_sync.py`

#### UNIX

More information available at [Wiki](https://github.com/frappe/biometric-attendance-sync-tool/wiki/Running-this-script-in-production)

### Setting Up Config

- Copy `local_config.py.template` and rename it to `local_config.py`
- Fill in the relevant details as described in the file
- Key configurations:
  - **ERPNext Connection:**
    - `ERPNEXT_API_KEY`: ERPNext user API Key
    - `ERPNEXT_API_SECRET`: ERPNext user API Secret
    - `ERPNEXT_URL`: ERPNext URL, e.g., `'https://yourcompany.erpnext.com'`, `'https://erp.yourcompany.com'`
    - `ERPNEXT_VERSION`: ERPNext version (e.g., 12, 13, 14)
  - **Script Settings:**
    - `PULL_FREQUENCY`: Frequency to pull data from the biometric device (in minutes)
    - `LOGS_DIRECTORY`: Directory for storing logs
    - `IMPORT_START_DATE`: Start date for importing data (`YYYYMMDD` format). Set `None` to import all available data.

#### Important Note on Start Date

**The start date is crucial and cannot be set to a past date.**
**If running the script on a new machine, ensure the start date follows the last recorded entry on the previous machine.**

### Resources

- [ERPNext Documentation](https://docs.erpnext.com/docs/user/manual/en/setting-up/articles/integrating-erpnext-with-biometric-attendance-devices)

- Project Wiki: [/Wiki](https://github.com/frappe/biometric-attendance-sync-tool/wiki)

### License

This project is licensed under the [GNU General Public License v3.0](LICENSE)

---

## Thai Version / ภาษาไทย

Python Scripts สำหรับดึงข้อมูลจากระบบบันทึกเวลาไบโอเมตริก _(BAS)_ และซิงค์กับระบบ ERPNext

### สารบัญ

- [ข้อกำหนดเบื้องต้น](#pre-requisites)
- [วิธีใช้งาน](#usage)
- [การตั้งค่า (สำหรับ CLI)](#setup-specifications-for-cli)
  - [UNIX](#unix)
- [การตั้งค่าคอนฟิก](#setting-up-config)
- [แหล่งข้อมูล](#resources)
- [ใบอนุญาต](#license)

### ข้อกำหนดเบื้องต้น

- Python 3.6+

### วิธีใช้งาน

ไฟล์ `erpnext_sync.py` เป็นแกนหลักของโครงการนี้ ดูข้อมูลเพิ่มเติมที่ [/Wiki](https://github.com/frappe/biometric-attendance-sync-tool/wiki)

### การตั้งค่า (สำหรับ CLI)

1. ติดตั้ง Dependencies:

   ```bash
   cd biometric-attendance-sync-tool
     && python3 -m venv venv
     && source venv/bin/activate
     && pip install -r requirements.txt
   ```

2. ตั้งค่า `local_config.py`:
   คัดลอกไฟล์ `local_config.py.template` และเปลี่ยนชื่อไฟล์ ดูข้อมูลเพิ่มเติมที่ [การตั้งค่าคอนฟิก](#setting-up-config)
3. รันสคริปต์โดยใช้ `python3 erpnext_sync.py`

#### ระบบปฏิบัติการ UNIX

มีข้อมูลเพิ่มเติมใน [Wiki](https://github.com/frappe/biometric-attendance-sync-tool/wiki/Running-this-script-in-production)

### การตั้งค่าคอนฟิก

- คัดลอกไฟล์ `local_config.py.template` และเปลี่ยนชื่อเป็น `local_config.py`
- กรอกข้อมูลที่เกี่ยวข้องตามคำอธิบายในไฟล์
- คีย์ที่สำคัญใน `local_config.py` มีดังนี้:
  - **การเชื่อมต่อกับ ERPNext:**
    - `ERPNEXT_API_KEY`: API Key ของผู้ใช้ ERPNext
    - `ERPNEXT_API_SECRET`: API Secret ของผู้ใช้ ERPNext
    - `ERPNEXT_URL`: URL ของ ERPNext เช่น `'https://yourcompany.erpnext.com'`, `'https://erp.yourcompany.com'`
    - `ERPNEXT_VERSION`: เวอร์ชันของ ERPNext เช่น 12, 13, 14
  - **การตั้งค่าสคริปต์:**
    - `PULL_FREQUENCY`: ความถี่ในการดึงข้อมูลจากเครื่องสแกนไบโอเมตริก (หน่วย: นาที)
    - `LOGS_DIRECTORY`: ไดเรกทอรีสำหรับจัดเก็บล็อก
    - `IMPORT_START_DATE`: วันที่เริ่มนำเข้าข้อมูล (รูปแบบ: `YYYYMMDD`)

#### หมายเหตุสำคัญเกี่ยวกับวันที่เริ่มต้น

**วันที่เริ่มต้นมีความสำคัญ ไม่สามารถตั้งเป็นวันที่ผ่านมาแล้วได้**
**หากใช้งานสคริปต์นี้บนเครื่องใหม่ ต้องกำหนดวันที่เริ่มต้นให้เป็นวันที่หลังจากวันที่สุดท้ายของเครื่องก่อนหน้า**

### แหล่งข้อมูล

- [ERPNext Documentation](https://docs.erpnext.com/docs/user/manual/en/setting-up/articles/integrating-erpnext-with-biometric-attendance-devices)

- Wiki ของโปรเจคนี้ [/Wiki](https://github.com/frappe/biometric-attendance-sync-tool/wiki)

### ใบอนุญาต

โครงการนี้อยู่ภายใต้ [GNU General Public License v3.0](LICENSE)
