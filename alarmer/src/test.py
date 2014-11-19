import sys
sys.path.append("./alarmer")

from alarmer import Main

main = Main(name="RAM")

informers = [
    main.Console(message = "Fuck, mem is $value!", delay = 5)
]

main.Ram(
    validate = lambda x: x.value < 20,
    informers = informers
)

main.run()