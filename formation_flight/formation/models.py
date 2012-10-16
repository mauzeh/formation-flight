"""Models contain information and do not initiate actions or commands.""" 

class Formation(list):
    """A bundle of flights."""
    
    def get_debug_lines(self):
        """Customize debug output"""
        lines = []
        for aircraft in self:
            lines.append(('%s' % aircraft, aircraft.description))
        return lines