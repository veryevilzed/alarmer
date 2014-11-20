import sys
sys.path.append("./alarmer")

from alarmer import Main

main = Main(name="RAM")

informers = [
    main.Console(message = "[$datetime] $msg_from wrote fuck, mem is $value!", delay = 5)
]

main.Ram(
    validate = lambda x: x["value"] < 80,
    informers = informers
)

main.run()