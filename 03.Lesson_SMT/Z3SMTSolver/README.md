# Exercise Z3

- [x] Follow the [Z3 Playground](https://jfmc.github.io/z3-play/) up to Bitvectors (don't read Bitvectors).

> :warning: Some browsers might not run the playground properly. Safari is a browser we know doesn't work well. Chrome, Chromium, Firefox, and Brave browsers have been tested to work fine.

- [x] Use Z3 to find a solution for the following puzzle:
</br>
<img src="images/Logic_Puzzle1.png" width="350">

- [x] Write a formula to check if the following two equations are equivalent:
</br>
<img src="images/Logic_Puzzle2.png" width="350">

- [x] A good additional practice will be to try and prove questions in [this file](AdditionalExerciseForSMT.pdf)

> :information_source: You might find the [cheat sheet](Cheat_Sheet.md) useful for the exercises and additional explanations of the Z3 principles.



Task #1
```
(declare-const a Int)
(declare-const b Int)
(declare-const c Int)
(assert (= (+ a a) 10))
(assert (= (+ (* a b) b) 12))
(assert (= (- (* a b) (* c a)) a))
(check-sat)
(get-model)
```

```
sat
(
  (define-fun a () Int
    5)
  (define-fun c () Int
    1)
  (define-fun b () Int
    2)
)
```

Task #2
```
(declare-const p Bool)
(declare-const q Bool)

(assert (= (= (and p q) p) (=> p q)))
(check-sat)
```

```
sat
```

Quiz:
```
(declare-const q Bool)
(declare-const p Bool)
(declare-const r Bool)

(echo "# Question 1")
(echo "p => q == !p ^ !q")
(push)
; SAT if there is case p => q == !p ^ !q
(assert (= (=> p q) (and (not p) (not q))))
(check-sat)
(pop)
(push)
; SAT if there is case p => != !p ^ !q
(assert (not (= (=> p q) (and (not p) (not q)))))
(check-sat)
(pop)

(echo "p => q == p ^ q")
(push)
; SAT if there is case p => q == p ^ q
(assert (= (=> p q) (and p q)))
(check-sat)
(pop)
(push)
; SAT if there is case p => != p ^ q
(assert (not (= (=> p q) (and p q))))
(check-sat)
(pop)

(echo "p => q == !p ^ q")
(push)
; SAT if there is case p => q == !p ^ q
(assert (= (=> p q) (and (not p) q)))
(check-sat)
(pop)
(push)
; SAT if there is case p => != !p ^ q
(assert (not (= (=> p q) (and (not p) q))))
(check-sat)
(pop)

(echo "# Question 2")
(push)
(echo "p v q => p")
(assert (=> (or p q) p))
(check-sat)
(pop)
(push)
(echo "p v q => p")
(assert (not (=> (or p q) p)))
(check-sat)
(pop)

(echo "# Question 3")
(push)
(echo "(p ^ (q v !p)) ^ !q")
(assert (and (and p (or q (not p))) (not q)))
(check-sat)
(pop)

(echo "# Question 4")
(push)
(echo "!(!p v !q v !r) <=> p ^ q ^ r")
(assert (= (not (or (not p) (not q) (not r))) (and p q r)))
(check-sat)
(pop)
(push)
(echo "!(!p v !q v !r) != p ^ q ^ r")
(assert (not (= (not (or (not p) (not q) (not r))) (and p q r))))
(check-sat)
(pop)


(echo "# Question 5")
(push)
(echo "!((!p v q) ^ (p v !q))")
(assert (not (and (or (not p) q) (or p (not q)))))
(check-sat)
(pop)
(push)
(echo "!((!p v q) ^ (p v !q))")
(assert (not (not (and (or (not p) q) (or p (not q))))))
(check-sat)
(pop)


(echo "# Question 6")
(push)
(echo "!((p ^ q) v (!p ^ !q))")
(assert (not (or (and p q) (and (not p) (not q)))))
(check-sat)
(pop)
(push)
(echo "!((p ^ q) v (!p ^ !q))")
(assert (not (not (or (and p q) (and (not p) (not q))))))
(check-sat)
(pop)


(echo "# Question 7")
(push)
(echo "p v !p => p v !p")
(assert (=> (or p (not p)) (or p (not p))))
(check-sat)
(pop)
(push)
(echo "p ^ !p => p v !p")
(assert (=> (and p (not p)) (or p (not p))))
(check-sat)
(pop)
(push)
(echo "(p ^ !p) v !p => p v !p")
(assert (=> (or (and p (not p)) (not p)) (or p (not p))))
(check-sat)
(pop)
(push)
(echo "(!p v p) ^ !p => p v !p")
(assert (=> (and (or (not p) p) (not p)) (or p (not p))))
(check-sat)
(pop)

(echo "# Question 8")
(push)
(echo "p ^ !p => p v !p")
(assert (=> (and p (not p)) (or p (not p))))
(check-sat)
(pop)
(push)
(echo "p ^ !p => p ^ !p")
(assert (=> (and p (not p)) (and p (not p))))
(check-sat)
(pop)
(push)
(echo "p ^ !p => (p ^ !q) v !r")
(assert (=> (and p (not p)) (or (and p (not q)) (not r))))
(check-sat)
(pop)
(push)
(echo "p ^ !p => (!p v p) ^ !p")
(assert (=> (and p (not p)) (and (or (not p) p) (not p))))
(check-sat)
(pop)

(echo "# Question 9")
(push)
(assert (=> (=> p (=> q r)) (=> (=> p q) r)))
(check-sat)
(pop)
(push)
(assert (not (=> (=> p (=> q r)) (=> (=> p q) r))))
(check-sat)
(pop)

(echo "# Question 10")
(push)
(assert (=> (=> (=> p q) r) (=> p (=> q r))))
(check-sat)
(pop)
(push)
(assert (not (=> (=> (=> p q) r) (=> p (=> q r)))))
(check-sat)
(pop)
```
