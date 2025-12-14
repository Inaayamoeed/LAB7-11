class ITTicket:
    """Represents an IT support ticket."""
    
    def __init__(self, ticket_id: int, title: str, priority: str, 
                 status: str, assigned_to: str):
        self.__id = ticket_id
        self.__title = title
        self.__priority = priority
        self.__status = status
        self.__assigned_to = assigned_to
    
    def get_id(self) -> int:
        return self.__id
    
    def get_title(self) -> str:
        return self.__title
    
    def get_priority(self) -> str:
        return self.__priority
    
    def get_status(self) -> str:
        return self.__status
    
    def get_assigned_to(self) -> str:
        return self.__assigned_to
    
    def assign_to(self, staff: str) -> None:
        """Assign ticket to a staff member."""
        self.__assigned_to = staff
    
    def close_ticket(self) -> None:
        """Mark ticket as closed."""
        self.__status = "Closed"
    
    def reopen_ticket(self) -> None:
        """Reopen a closed ticket."""
        if self.__status == "Closed":
            self.__status = "Open"
    
    def __str__(self) -> str:
        return (
            f"Ticket {self.__id}: {self.__title} "
            f"[{self.__priority}] – {self.__status} (assigned to: {self.__assigned_to})"
        )
    
    def __repr__(self) -> str:
        return self.__str__()