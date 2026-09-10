package mission

import "fmt"

type Status string

const (
	Open      Status = "open"
	Waiting   Status = "waiting"
	Running   Status = "running"
	Done      Status = "done"
	Failed    Status = "failed"
	HandedOff Status = "handed_off"
)

func ParseStatus(s string) (Status, error) {
	st := Status(s)
	switch st {
	case Open, Waiting, Running, Done, Failed, HandedOff:
		return st, nil
	default:
		return "", fmt.Errorf("unknown status %q", s)
	}
}

func IsTerminal(s Status) bool {
	return s == Done || s == Failed || s == HandedOff
}

var allowed = map[Status]map[Status]bool{
	Open: {
		Waiting:   true,
		Running:   true,
		Done:      true,
		Failed:    true,
		HandedOff: true,
	},
	Waiting: {
		Running:   true,
		Done:      true,
		Failed:    true,
		HandedOff: true,
	},
	Running: {
		Waiting:   true,
		Done:      true,
		Failed:    true,
		HandedOff: true,
	},
}

// Transition returns an error if from → to is illegal.
// Same-status is a no-op.
func Transition(from, to Status) error {
	if from == to {
		return nil
	}
	if IsTerminal(from) {
		return fmt.Errorf("illegal status transition %s -> %s", from, to)
	}
	if allowed[from][to] {
		return nil
	}
	return fmt.Errorf("illegal status transition %s -> %s", from, to)
}
