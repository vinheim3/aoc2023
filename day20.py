from math import lcm

from common import get_input


class FlipFlop:
    def __init__(self, name, dests):
        self.state = 0
        self.name = name
        self.dests = dests

    def recv(self, sender, is_high):
        if not is_high:
            self.state = 1 - self.state
            return self.state == 1
        return None


class Conjunction:
    def __init__(self, name, dests):
        self.states = {}
        self.name = name
        self.dests = dests

    def recv(self, sender, is_high):
        self.states[sender] = 1 if is_high else 0
        return set(self.states.values()) != {1}


class Broadcaster:
    def __init__(self, name, dests):
        self.name = name
        self.dests = dests

    def recv(self, sender, is_high):
        return is_high


if __name__ == "__main__":
    modules = {}
    conjunctions = set()
    for entry in get_input(20):
        name, dests = entry.split(" -> ")
        dests = dests.split(", ")
        if name.startswith('%'):
            name = name[1:]
            modules[name] = FlipFlop(name, dests)
        elif entry.startswith('&'):
            name = name[1:]
            modules[name] = Conjunction(name, dests)
            conjunctions.add(name)
        else:
            modules[name] = Broadcaster(name, dests)

    # Set Conjunction parents' state
    for k, v in modules.items():
        for dest in v.dests:
            if dest in conjunctions:
                modules[dest].states[k] = 0

    total = {True: 0, False: 0}

    def press_btn():
        pulses_sent = [("button", "broadcaster", False)]
        sent_low = set()  # for part 2
        while pulses_sent:
            sender, name, is_high = pulses_sent.pop(0)
            if is_high is False:
                sent_low.add(sender)
            total[is_high] += 1
            if name in ('rx', 'output'):
                continue
            module = modules[name]
            ret = module.recv(sender, is_high)
            if ret is not None:
                for dest in module.dests:
                    pulses_sent.append((name, dest, ret))
        return sent_low

    for i in range(1000):
        sent_low = press_btn()

    print("Part 1:", total[True] * total[False])

    i += 1
    must_be_low = {'hr', 'gl', 'nr', 'gk'}
    first_seen = {}
    while 1:
        sent_low = press_btn()
        i += 1

        lows = must_be_low & sent_low
        for low in lows:
            if low not in first_seen:
                first_seen[low] = i
                if len(first_seen.items()) == 4:
                    print("Part 2:", lcm(*first_seen.values()))
                    exit(0)
