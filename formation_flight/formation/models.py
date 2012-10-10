class Formation(list):
    
    def get_debug_lines(self):
        """Customize debug output"""
        lines = []
        for aircraft in self:
            lines.append(('%s' % aircraft, aircraft.description))
        return lines
