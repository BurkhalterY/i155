import pygame
joystick = pygame.joystick
event = pygame.event

pygame.get_init() or pygame.init()
joystick.get_init() or joystick.init()

JOYAXISMOTION = pygame.JOYAXISMOTION
JOYBALLMOTION = pygame.JOYBALLMOTION
JOYBUTTONDOWN = pygame.JOYBUTTONDOWN
JOYBUTTONUP = pygame.JOYBUTTONUP
JOYHATMOTION = pygame.JOYHATMOTION

_joystick_events = [
    JOYAXISMOTION,
    JOYBALLMOTION,
    JOYBUTTONDOWN,
    JOYBUTTONUP,
    JOYHATMOTION,
]

_joysticks : dict[int, Joystick] = {}

class Joystick:
    '''Represents a joystick for the game

    Use events to automatically call functions when something happens
    (This part depends on pygame's goodwill)
    '''

    _events : dict[int, list[callable[event.EventType, None]]] = {}
    _id : int

    _axis : dict[int, float] = {}
    _balls : dict[int, tuple[float, float]] = {}
    _buttons : dict[int, bool] = {}
    _hats : dict[int, tuple[float, float]] = {}

    def __init__(self, jid: int):
        if jid in _joysticks:
            return _joysticks[jid]
        if jid < 0:
            raise IndexError("No joystick id can be below 0")

        self._id = jid
        _joysticks[jid] = self

        self.refresh()

        def update_axis(event: event.Event):
            i : int = event.axis
            if not i in self._axis:
                return
            val : float = event.value
            self._axis[i] = val

        # No ball support
        #def update_ball(event: event.Event):
            #print(event)

        def update_button_down(event: event.Event):
            i : int = event.button
            if not i in self._buttons:
                return
            self._buttons[i] = True

        def update_button_up(event: event.Event):
            i : int = event.button
            if not i in self._buttons:
                return
            self._buttons[i] = False

        # No hat support
        #def update_hat(event: event.Event):
            #return

        self.add_event(JOYAXISMOTION, update_axis)
        #self.add_event(JOYBALLMOTION, update_ball)
        self.add_event(JOYBUTTONDOWN, update_button_down)
        self.add_event(JOYBUTTONUP, update_button_up)
        #self.add_event(JOYHATMOTION, update_hat)

    def reset(self, erase: bool = True):
        '''Resets the joystick's values

        Params
        ------
        erase: bool
            Does nothing if the joystick exists
            If true and the joystick doesn't exist, all values will be empty
            If false and the joystick doesn't exist, nothing will happen
        '''
        if 0 <= self._id < joystick.get_count() or erase:
            self._axis : dict[int, float] = {}
            self._balls : dict[int, tuple[float, float]] = {}
            self._buttons : dict[int, bool] = {}
            self._hats : dict[int, tuple[float, float]] = {}
        if self._id >= joystick.get_count():
            return

        j = joystick.Joystick(self._id)

        # Set everything to 0
        for i in range(j.get_numaxes()):
            self._axis[i] = 0.0
        for i in range(j.get_numballs()):
            self._balls[i] = (0.0, 0.0)
        for i in range(j.get_numbuttons()):
            self._buttons[i] = False
        for i in range(j.get_numhats()):
            self._hats[i] = (0.0, 0.0)

    def refresh(self):
        '''Refreshes the joystick's contents

        Assumes the event queue has been processed
        '''
        self.reset()

        jid = self._id
        if 0 > jid or jid >= joystick.get_count():
            # You can't fetch something that doesn't exist
            return

        j = joystick.Joystick(jid)
        j.init()
        for i in range(j.get_numaxes()):
            self._axis[i] = j.get_axis(i)
        for i in range(j.get_numballs()):
            self._balls[i] = j.get_ball(i)
        for i in range(j.get_numbuttons()):
            self._buttons[i] = j.get_button(i)
        for i in range(j.get_numhats()):
            self._hats[i] = j.get_hat(i)

    def add_event(self, event_id: int, func: callable[event.EventType, None]):
        self._events[event_id] += [func]

    def remove_event(self, event_id: int, func: callable[event.EventType, None]):
        events = self._events[event_id]
        if func in events:
            events.remove(func)

    def _call_event(self, event_id: int, event: event.EventType):
        '''Calls the registered events

        Params
        ------
        event_id: int
            Id of the event whose functions are to call
        '''
        if not event_id in self._events:
            return

        if not 'joy' in event.dict:
            return

        if event.joy != self._id:
            return

        for f in self._events[event_id]:
            f(event)

    def get_axis(self, axis: int) -> float:
        pass

    def get_ball(self, ball: int) -> tuple[float, float]:
        pass

    def get_button(self, button: int) -> bool:
        pass

    def get_hat(self, hat: int) -> tuple[float, float]:
        pass

def refresh_joysticks():
    '''"Refreshes" the joysticks by calling the most recent joystick events

    /!\\ Make sure to not call `pygame.event.get` with any joystick event ids, or `pygame.event.dump` /!\\
    '''
    # Call the functions
    for event_id in _joystick_events:
        events = event.get(event_id)
        for e in events:
            for j in _joysticks.values():
                j._call_event(event_id, e)
