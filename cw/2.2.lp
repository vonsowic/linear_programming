clear
end 2*x1 + x2
maximize 1

add 2*x1 + x2 <= 4
add 2*x1 + 3*x2 <= 3
add 4*x1 + x2 <= 5
add x1 + 5*x2 <= 1
add x1 >= 0
add x2 >= 0

# w celach optymalizacyjnych
radian 3

multithreading 1
sizethreads 4
show
execute
exit
