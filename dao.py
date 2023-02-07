def insert_item(engine, stmt):
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()

    return result.inserted_primary_key