async def update_state_data(state, data):
    await state.reset_data()
    await state.update_data(**data)
