from fastapi import APIRouter, Depends, HTTPException
from server.app.models import Order, User, OrderItem
from server.app.schemas import OrderSchema, ItemOrderSchema
from server.app.dependencies import catch_session, check_token
from sqlalchemy.orm import Session

order_router = APIRouter(prefix="/orders", tags=["Orders"], dependencies=[Depends(check_token)])

@order_router.get("/")
async def orders():
    '''
    This is the systems default order route. All order routes need authentication.
    '''
    return{'message': 'You accessed the orders route'}

@order_router.post('/order')
async def create_order(order_schema: OrderSchema, session: Session = Depends(catch_session)):
    new_order = Order(user = order_schema.user)
    session.add(new_order)
    session.commit()
    return {'message': f'Order created successfully. Order ID:{new_order.id}'}

@order_router.post('/order/cancel/{id_order}')
async def cancel_order(id_order: int, session: Session = Depends(catch_session), user: User = Depends(check_token)):
    order = session.query(Order).filter(Order.id == id_order).first()
    if not order:
        raise HTTPException(status_code=400, detail='Order not found')

    if user.id != order.user and not user.admin:
        raise HTTPException(status_code=401, detail='You dont have permission to make this change')
                            
    order.status = 'CANCELED'
    session.commit()
    return{
        'message': f'Order number: {order.id} successfully canceled',
        'Order': order
    }

@order_router.get('/list')
async def list_orders( session: Session = Depends(catch_session), user: User = Depends(check_token)):
    if not user.admin:
        raise HTTPException(status_code=401, detail='You dont have permission')
    else:
        order = session.query(Order).all()
        return{
            'orders': order
        }

@order_router.post('/order/add/{id_order}')
async def add_item(id_order: int, itemSchema: ItemOrderSchema, session: Session = Depends(catch_session), user: User = Depends(check_token)):
    order = session.query(Order).filter(Order.id == id_order).first()
    if not order:
        raise HTTPException(status_code= 401, detail='Order doesnt exist')

    if user.id != order.user and not user.admin:
        raise HTTPException(status_code=401, detail='You dont have permission')

    item_order = OrderItem(itemSchema.quantity, itemSchema.flavor, itemSchema.size, itemSchema.unit_price, id_order)
    order.calculate_price()
    session.add(item_order)
    session.commit()
    return {
        'message': 'Item created successfully',
        'item_id': item_order.id,
        'price_order': order.price 
    }

@order_router.post('/order/remove/{id_item_order}')
async def remove_item(id_item_order: int, session: Session = Depends(catch_session), user: User = Depends(check_token)):
    item_order = session.query(OrderItem).filter(OrderItem.id == id_item_order).first()
    order = session.query(Order).filter(Order.id == item_order.order).first()
    if not item_order:
        raise HTTPException(status_code= 401, detail='Item doesnt exist')

    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail='You dont have permission')

    session.delete(item_order)
    order.calculate_price()
    session.commit()
    return {
        'message': 'Item removed successfully',
        'item_quantity': len(order.items),
        'order': order 
    }

@order_router.post('/order/finished/{id_order}')
async def finished_order(id_order: int, session: Session = Depends(catch_session), user: User = Depends(check_token)):
    order = session.query(Order).filter(Order.id == id_order.order).first()
    if not order:
        raise HTTPException(status_code= 401, detail='Order doesnt exist')

    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail='You dont have permission')

    order.status = 'FINISHED'
    session.commit()
    return {
        'message': f'Order number: {order.id} successfully completed',
        'order': order 
    }
