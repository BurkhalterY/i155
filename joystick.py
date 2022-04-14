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
            self.events[event_id] = []
        self.events[event_id] += [func]

    def remove_event(self, event_id, func):
        if not event_id in self.events:
            return
        events = self.events[event_id]
        if func in events:
            events.remove(func)

    def call_event(self, event_id, event):
        '''Calls the registered events

        Params
        ------
        event_id: int
            Id of the event whose functions are to call
        '''
        if not event_id in self.events:
            return

        if not 'joy' in event.dict:
            return

        if event.joy != self.id:
            return

        for f in self.events[event_id]:
            f(event)
