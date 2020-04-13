"""flight modelling"""

class Flight:
    """A flight with some aircraft"""
    
    def __init__(self,number,aircraft):
        
        """checkin for class INVARIANTS"""
        if not number[:2].isalpha():
            raise ValueError(f"No Airline code in number '{number}'")
            
        if not number[:2].isupper():
            raise ValueError(f"Invalid Airline code in '{number}'")
        
        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError(f"Invalid route number '{number}'")
        
        self._number = number
        self._aircraft = aircraft
        rows, seat_letters = self._aircraft.seating_plan()
        self._seating = [None] + [{letter:None for letter in seat_letters} for _ in rows]
    
    def number(self):
        return self._number
    
    def airline(self):
        return self._number[2:]

    def aircraft_model(self):
        return self._aircraft.model()
    
    def allocate_seat(self, seat, passenger):
        
        row, letter = self._parse_seat(seat)
                
        if self._seating[row][letter] != None:
            raise ValueError(f"seat {seat} taken")
            
        self._seating[row][letter] = passenger
        
    def _parse_seat(self,seat):
         
        rows, seat_letters = self._aircraft.seating_plan()
        
        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError(f"Invalid seat letter {letter}")
        
        row_txt = seat[:-1]
        try:
            row = int(row_txt)
        except ValueError:
            raise ValueError(f"Invalid seat row")
            
        if row not in rows:
            raise ValueError(f"Invalid row number")

        if letter not in seat_letters:
            raise ValueError(f"Invalid row letter")
    
        return row, letter
    
    def relocate_passenger(self, from_seat, to_seat):
        
        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] == None:
            raise ValueError(f"No passenger in {from_seat}")
            
        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] != None:
            raise ValueError(f"{to_seat} is already taken")
        
        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None
        
    def num_avaiable_seats(self):
        return sum(sum(1 for el in row.values() if el is None)
                for row in self._seating if row != None)
         
       
    def make_boarding_pass(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(), self.aircraft_model())
    
    def _passenger_seats(self):
        """iterable for seat locations"""
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger != None:
                    yield (passenger, f"{row}{letter}")
        
    
    
    
class Aircraft:
    
    def __init__(self, reg, mod, n_rows, n_seats_per_row):
        self._reg = reg
        self._mod = mod
        self._n_rows = n_rows
        self._n_seats_per_row = n_seats_per_row
        
    def registration(self):
        return self._reg
    
    def model(self):
        return self._mod
    
    def seating_plan(self):
        return (range(1,self._n_rows+1),
                'ABCDEFGHJK'[:self._n_seats_per_row])
    
    
    
def console_card_printer(passenger, seat, flight_no, aircraft):
    
    output = f" Name: {passenger}" \
             f" Flight: {flight_no}" \
             f" Seat: {seat}" \
             f" Aircraft: {aircraft}"
    
    banner = '+' + '-' * (len(output)-2) + "+"
    border = '|' + ' ' * (len(output)-2) + "|"
    
    lines = [banner, border, output, border, banner]
    card = '\n'.join(lines)
    print(card)
    print()
    
    
    
    
    
        