import os

ROWS = ["A", "B", "C"]
SEATS_PER_ROW = 5
TICKET_PRICE = 200
BOOKING_FILE = "bookings.txt"
TOTAL_SEATS = len(ROWS) * SEATS_PER_ROW

# 2D list: seat_map[row][col] 
seat_map = [["_"] * SEATS_PER_ROW for _ in ROWS]
# seat code -> customer name
bookings = {}

def create_empty_hall():
    """Reset the seat map and bookings so the hall is empty."""
    global seat_map, bookings
    seat_map = [["_"] * SEATS_PER_ROW for _ in ROWS]
    bookings = {}


def parse_seat(code):
    """Validate a seat code like 'Al', Returns (row_idx, col_idx) or None,"""
    code = code.strip().upper()
    if len(code) != 2:
        return None
    row, num = code[0], code[1]
    if row not in ROWS or not num.isdigit():
        return None
    n = int(num)
    if n < 1 or n > SEATS_PER_ROW:
        return None
    return ROWS.index(row), n - 1


def seats_left():
    """Count free seats."""
    return sum(row.count("_") for row in seat_map)


def save_bookings():
    """ Write all bookings to the file (called after every change)."""
    with open(BOOKING_FILE, "w") as f:
        for seat, name in bookings.items():
            f.write(f"{seat},{name}\n")


def load_bookings():
    """ Load bookings from the file at start and mark them on the seat map."""
    create_empty_hall()
    if not os.path.exists(BOOKING_FILE):
        return
    with open(BOOKINGS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "," not in line:
                continue
            seat, name = line.split(",", 1)
            pos = parse_seat(seat)
            if pos is not None and seat_map[pos[0]][pos[1]] == "_":
                seat_map[pos[0]][pos[1]] = "X"
                bookings[seat.strip().upper()] = name.strip()


def book_seats(seat_codes, name):
    """ Book one more seats for a customer. Returns True if all booked."""
    # validate everything first so a bad entry books nothing
    positions = []
    for code in seat_codes:
        pos = parse_seat(code)
        if pos is None:
            print("Invalid seat. Rows are A to C and seat numbers are 1 to 5.")
            return False
        r, c = pos
        if seat_map[r][c] == "X" or code.strip().upper() in positions:
            print(f"Seat {code.strip().upper()} is already booked.")
            return False
        positions.append(code.strip().upper())

    for code in positions:
        r, c = parse_seat(code)
        seat_map[r][c] = "X"
        bookings[code] = name
    save_bookings()

    amount = len(positions) * TICKET_PRICE
    print(f"Seat{'s' if len(positions) > 1 else ''}" f"{','.join(positions)} booked for {name}. Amount: {amount}")
    left = seats_left()
    if left == 0:
        print("Seats left: 0")
        print("Show is now housefull.")
    return True


def cancel_booking(code):
    """Cancel a booked seat,"""
    pos = parse_seat(code)
    if pos is None:
        print("Invalid seat. Rows are A to C and seat numbers are 1 to 5.")
        return Fallse
    r, c = pos
    code = code.strip().upper()
    if seat_map[r][c] == "_":
        print(f"Seat {code} is not booked.")
        return False
    seat_map[r][c] = "_"
    name = bookings.pop(code, "")
    save_bookings()
    print(f"Booking of seat {code} ({name}) cancelled. Refunf: {TICKET_PRICE}")
    return True


def display_seat_map():
    """Print the seat map (X = booked, _ = free) and seats left."""
    print("   " + " ".join(str(i) for i in range(1, SEATS_PER_ROW + 1)))
    for i, row in enumerate(seat_map):
        print(f"Row {ROWS[i]}: " + " ".join(row))
    print(f"Seats left: {seats_left()}")


def show_menu():
    print("\n===== MOVIE TICKET BOOKING =====")
    print("1. Book")
    print("2. Cancel")
    print("3. Seat map")
    print("4. Exit")


def main():
    load_bookings()
    while True:
        show_menu()
        choice = input("Enter choice: ").strip()
        if choice == "1":
            codes = input("Seat(s) (e.g. A1 OR A2 A3): ").replace(",", " ").split()
            if not codes:
                print("Invalid seat. Rows are A to C and seat numbers are 1 to 5.")
                continue
            name = input("Name: ").strip()
            book_seats(codes, name)
        elif choice == "2":
            cancel_booking(input("Seat to cancel: "))
        elif choice == "3":
            display_seat_map()
        elif choice == "4":
            print("Thank you! Bookings saved to", BOOKING_FILE)
            break
        else:
            print("Invalid option. Choose 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
    




    