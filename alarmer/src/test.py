from alarmer import Main

main = Main(name="RAM")

email = main.Informer(
    message = "Hello!"
)

informers = [email]



main.Ram(
    validate = lambda v: v < 70
    informers = informers
)

main.run()