# Loader: Insert cleaned data into DB
from backend.db.models import Company, UploadedFile, DailyPrice
from sqlalchemy.orm import Session
import hashlib
import datetime


def load_data(dfs, date_str, filename, session: Session, force_reprocess=False):
    errors = []
    companies = set()
    rows_inserted = 0
    # Compute md5
    with open(filename, 'rb') as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    # Check for duplicate file
    existing_file = session.query(UploadedFile).filter_by(md5=md5).first()
    if existing_file:
        if force_reprocess:
            # Delete previous record and associated daily prices
            session.query(DailyPrice).filter_by(source_file_id=existing_file.id).delete()
            session.delete(existing_file)
            session.commit()
        else:
            errors.append("File already processed.")
            return {'companies': 0, 'rows_inserted': 0, 'errors': errors}
    # Insert UploadedFile
    uploaded_file = UploadedFile(filename=filename, upload_date=datetime.datetime.now(), md5=md5, rows_extracted=0, success=False)
    session.add(uploaded_file)
    session.commit()
    # Convert date_str to Python date object
    date_obj = None
    if date_str:
        try:
            date_obj = datetime.datetime.strptime(date_str, "%B %d, %Y").date()
        except Exception:
            date_obj = None
    for df in dfs:
        from backend.etl.data_cleaner import clean_dataframe
        df = clean_dataframe(df)
        for _, row in df.iterrows():
            symbol = row['Symbol']
            companies.add(symbol)
            # Upsert company
            company = session.query(Company).filter_by(symbol=symbol).first()
            if not company:
                company = Company(symbol=symbol)
                session.add(company)
                session.commit()
            # Insert daily price
            try:
                dp = DailyPrice(
                    company_id=company.id,
                    date=date_obj,
                    pclose=row.get('PClose'),
                    open=row.get('Open'),
                    high=row.get('High'),
                    low=row.get('Low'),
                    close=row.get('Close'),
                    change=row.get('Change'),
                    deals=row.get('Deals'),
                    volume=row.get('Volume'),
                    value=row.get('Value'),
                    vwap=row.get('VWAP'),
                    source_file_id=uploaded_file.id
                )
                session.add(dp)
                rows_inserted += 1
            except Exception as e:
                errors.append(str(e))
    uploaded_file.rows_extracted = rows_inserted
    uploaded_file.success = (rows_inserted > 0)
    session.commit()
    return {'companies': len(companies), 'rows_inserted': rows_inserted, 'errors': errors}
