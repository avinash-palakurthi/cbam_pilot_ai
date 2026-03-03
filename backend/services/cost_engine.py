def calculate_cost(volume:float, emission_factor:float, ets_price:float):
    embedded_emission=volume * emission_factor
    cost=embedded_emission * ets_price
    
    return embedded_emission,cost