(define (domain strips-sliding-tile)
    (:requirements :strips)
    (:predicates 
        (tile ?t) 
        (position ?p)
        (at ?t ?x  ?y) 
        (blank ?x ?y)
        (inc ?to ?from )
        (dec ?to ?from )
    )

    (:action up
        :parameters 
            (?t 
            ?x
            ?y 
            ?new)
        :precondition
            (and (tile ?t) (position ?x) (position ?y) (position ?new) (at ?t ?x ?y)
            (blank ?x ?new) (dec ?new ?y))
        :effect (and (not (blank ?x ?new)) (not (at ?t ?x ?y))
             (blank ?x ?y) (at ?t ?x ?new)))

    (:action down
        :parameters 
            (?t
            ?x
            ?y
            ?new)
        :precondition
            (and (tile ?t) (position ?x) (position ?y) (position ?new) (at ?t ?x ?y)
            (blank ?x ?new) (inc ?new ?y))
        :effect (and (not (blank ?x ?new)) (not (at ?t ?x ?y))
             (blank ?x ?y) (at ?t ?x ?new)))

    (:action left
        :parameters 
            (?t 
            ?x 
            ?y 
            ?new)
        :precondition
            (and (tile ?t) (position ?x) (position ?y) (position ?new) (at ?t ?x ?y)
            (blank ?new ?y) (dec ?new ?x))
        :effect (and (not (blank ?new ?y)) (not (at ?t ?x ?y))
             (blank ?x ?y) (at ?t ?new ?y))) 

    (:action right
        :parameters 
            (?t 
            ?x 
            ?y 
            ?new)
        :precondition
            (and (tile ?t) (position ?x) (position ?y) (position ?new) (at ?t ?x ?y)
            (blank ?new ?y) (inc ?new ?x))
        :effect (and (not (blank ?new ?y)) (not (at ?t ?x ?y))
             (blank ?x ?y) (at ?t ?new ?y)))
)