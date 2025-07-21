import datetime

class State:
    def __init__(self, condition = None, expiration_date = None):
        self._condition = condition
        self._expiration_date = expiration_date

    def is_expired(self):
        if self._expiration_date:
            today = datetime.date.today()
            expiration = datetime.date(*self._expiration_date)
            return today > expiration
        return False
    
    def to_dict(self):
        state_dict = {}
        if self._condition is not None:
            state_dict["condition"] = self._condition
        if self._expiration_date is not None:
            state_dict["expiration_date"] = self._expiration_date
        return state_dict
    
    def __str__(self):
        state_parts = []
        if isinstance(self._condition, str):
            state_parts.append(f"Condition: {self._condition}")
        if self._expiration_date:
            date = datetime.date(*self._expiration_date)
            date_str = date.strftime("%Y-%m-%d")
            state_parts.append(f"Expires: {date_str}")
        return ", ".join(state_parts) if state_parts else "Unknown"
