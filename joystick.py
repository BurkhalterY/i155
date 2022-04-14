import pygame

class Joystick:
    '''Represents a joystick for the game

    Use events to automatically call functions when something happens
    (This part depends on pygame's goodwill)
    '''
    def __init__(self, jid):
        self.id = jid

        if 0 > jid or jid >= pygame.joystick.get_count():
            # You can't fetch something that doesn't exist
            return

        self.j = pygame.joystick.Joystick(jid)
        self.j.init()
        self.events = dict()

    def add_event(self, event_id, func):
        if not event_id in self.events:
            # Create event type if not exists
            self.events[event_id] = []
        self.events[event_id] += [func]  # Add function to event list

    def remove_event(self, event_id, func):
        if not event_id in self.events:
            # If this event type not exits, do nothing
            return
        events = self.events[event_id]
        if func in events:
            # If this event functino exit in list, remove it
            events.remove(func)

    def call_event(self, event_id, event):
        # No function for this event type -> return
        if not event_id in self.events:
            return

        # Not a joystick event type -> return
        if not 'joy' in event.dict:
            return

        # Joystick of event isn't the same as the current joystick -> return
        if event.joy != self.id:
            return

        # If all if are false
        # Execute all registered functions
        for f in self.events[event_id]:
            f(event)
