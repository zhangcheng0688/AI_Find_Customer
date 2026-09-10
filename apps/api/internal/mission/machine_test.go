package mission

import "testing"

func TestTransitionHappyPath(t *testing.T) {
	path := []Status{Open, Waiting, Running, Done}
	for i := 0; i < len(path)-1; i++ {
		if err := Transition(path[i], path[i+1]); err != nil {
			t.Fatalf("%s -> %s: %v", path[i], path[i+1], err)
		}
	}
}

func TestTransitionFromOpen(t *testing.T) {
	for _, to := range []Status{Waiting, Running, Done, Failed, HandedOff} {
		if err := Transition(Open, to); err != nil {
			t.Fatalf("open -> %s: %v", to, err)
		}
	}
}

func TestIllegalFromDone(t *testing.T) {
	if err := Transition(Done, Running); err == nil {
		t.Fatal("expected error")
	}
	if err := Transition(Failed, Open); err == nil {
		t.Fatal("expected error")
	}
	if err := Transition(HandedOff, Waiting); err == nil {
		t.Fatal("expected error")
	}
}

func TestIllegalSkippingRules(t *testing.T) {
	if err := Transition(Waiting, Open); err == nil {
		t.Fatal("waiting -> open should fail")
	}
	if err := Transition(Running, Open); err == nil {
		t.Fatal("running -> open should fail")
	}
}

func TestSameStatusNoop(t *testing.T) {
	if err := Transition(Running, Running); err != nil {
		t.Fatal(err)
	}
}

func TestParseStatus(t *testing.T) {
	if _, err := ParseStatus("nope"); err == nil {
		t.Fatal("expected error")
	}
	st, err := ParseStatus("handed_off")
	if err != nil || st != HandedOff {
		t.Fatalf("got %q %v", st, err)
	}
}
