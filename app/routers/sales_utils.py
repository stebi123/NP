from sqlalchemy.orm import Session
from app.models.batch_pallet import BatchPallet
from app.models.batch import Batch

def get_batch_pallets_for_sale(db: Session, product_id: int, fifo: bool):

    if fifo:
        # FIFO = oldest stored first
        return (
            db.query(BatchPallet)
            .join(Batch, Batch.id == BatchPallet.batch_id)
            .filter(
                Batch.product_id == product_id,
                BatchPallet.quantity_left > 0
            )
            .order_by(BatchPallet.stored_on.asc())
            .all()
        )

    else:
        # FEFO = nearest expiry first
        return (
            db.query(BatchPallet)
            .join(Batch, Batch.id == BatchPallet.batch_id)
            .filter(
                Batch.product_id == product_id,
                BatchPallet.quantity_left > 0
            )
            .order_by(Batch.expiry_date.asc())
            .all()
        )
