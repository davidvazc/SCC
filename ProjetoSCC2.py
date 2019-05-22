import salabim as sim
import random

n_placas_dia=int((5280+440*8)/22)
n_rodas_dia=int((2640*4+5280*4)/22)
n_produtos_dia=int((5280+2640+440)/22)
skates=0   
n_pranchas=0
n_rodas=0
Conjunto_pranchas=0
Conjunto_rodas=0
status="active"

#Relogio
class Clock(sim.Component):
    def process(self):
        global status
        while True:
            status="active"
            yield self.hold(8*60)
            status="inactive"
            yield self.hold(16*60)


#Generator
class Generator(sim.Component):
    def process(self):
        global status
        while (status=="active"):
            for _ in range(n_placas_dia):
                Placa()
                yield self.hold(sim.Uniform(5, 15).sample())
            for _ in range(n_rodas_dia):
                Roda()
                yield self.hold(sim.Uniform(5,15).sample())
            for _ in range(n_produtos_dia):    
                Finish()
                yield self.hold(sim.Uniform(5, 15).sample())
                    
                
#Etapas da placa
class Placa(sim.Component):
    def process(self):
        global n_pranchas
        #Fila de espera do pressing
        self.enter(presswaitingline)
        yield self.request((prensa, 4))
        self.leave(presswaitingline)
        #Pressing
        yield self.hold(100)
        self.release((prensa, 4))

        #Apos o pressing, meter no armazem
        self.enter(storage1_wl)
        yield self.hold(24*60)
        #Meter na fila de espera do cutting, após o pressing tar feito
        self.enter(cutwaitingline)
        yield self.request((trabalhador, 3))
        self.leave(cutwaitingline)
        storage1_wl.pop()
        #Cutting
        yield self.hold(60)
        self.release((trabalhador, 3))

        #Meter na fila de espera do finishing
        self.enter(finwaitingline)
        yield self.request((trabalhador, 1))
        self.leave(finwaitingline)
        #Finishing
        yield self.hold(15)
        self.release((trabalhador, 1))

        #Meter na fila de espera do Painting
        self.enter(paintwaitingline)
        yield self.request((trabalhador, 1))
        self.leave(paintwaitingline)
        #Painting
        yield self.hold(20)
        self.release((trabalhador, 1))

        #Ao fim da prancha tar pronta
        self.enter(storage2_wl)
        yield self.hold(24*60)
        n_pranchas+=24
        prancha.set_capacity(n_pranchas)
        
            
            
#Roda
class Roda(sim.Component):
    def process(self):
        global n_rodas
        #Entra na fila de espera de Foundry
        self.enter(foundrywaitingline)
        yield self.request((fornalha, 1))
        self.leave(foundrywaitingline)
        #Foundry
        yield self.hold(55)
        self.release((fornalha, 1))
        
        #Entra na storage 3
        self.enter(storage3_wl)
        yield self.hold(24*60)
        #Entra na fila de espera de Machining
        self.enter(machiningwaitingline)
        yield self.request((torno, 2))
        self.leave(machiningwaitingline)
        storage3_wl.pop()
        #Machining
        yield self.hold(60)
        self.release((torno,2))

        #Entra na fila de espera de Printing
        self.enter(printingwaitingline)
        yield self.request((impressora, 1))
        self.leave(printingwaitingline)
        #Printing
        yield self.hold(20)
        self.release((impressora, 1))
        
        #Entra na storage 4
        self.enter(storage4_wl)
        yield self.hold(24*60)
        n_rodas+=192
        rodas.set_capacity(n_rodas)
        
        
        
        
#Venda
class Finish(sim.Component):
    def process(self):
        global n_rodas
        global n_pranchas
        global skates
        global Conjunto_pranchas
        global Conjunto_rodas        
        escolha = random.choice(Final)
        if(escolha == "packingdecks"):
            self.enter(packdeckwaitingline)
            yield self.request( (trabalhador, 2) , (prancha,8*12) )
            self.leave(packdeckwaitingline)
            for _ in range(8*12):
                storage2_wl.pop()
            yield self.hold(10)
            self.release((trabalhador, 2))
            Conjunto_pranchas+=12
        elif(escolha == 'packingwheels'):
            self.enter(packwheelswaitingline)
            yield self.request((maq_embalagem, 1),(rodas,4*48))
            self.leave(packwheelswaitingline)
            for _ in range(4*48):
                storage4_wl.pop()
            yield self.hold(30)
            self.release((maq_embalagem, 1)) 
            Conjunto_rodas+=48        
    
        elif(escolha == "assembly"):
            self.enter(assemblywaitingline)
            yield self.request((trabalhador, 2),(prancha,24),(rodas,24*4))
            self.leave(assemblywaitingline)
            for _ in range(24):
                storage2_wl.pop()
            for _ in range(24*4):
                storage4_wl.pop()
            yield self.hold(30)
            self.release((trabalhador, 2))
            skates+=24           
        

env = sim.Environment(time_unit='minutes', trace=False)
Clock()
Generator()


#Recursos
prancha= sim.Resource("prancha_skate")
rodas= sim.Resource("rodas_skate")
trabalhador = sim.Resource("trabalhador", capacity = 5)
prensa = sim.Resource("prensa", capacity = 4)
fornalha = sim.Resource("fornalha", capacity = 1)
torno = sim.Resource("torno", capacity = 2)
impressora = sim.Resource("impressora", capacity = 1)
maq_embalagem = sim.Resource("maq_embalagem", capacity = 1)

#Filas de espera
storage1_wl = sim.Queue("storage1")
storage2_wl = sim.Queue("storage2")
storage3_wl = sim.Queue("storage3")
storage4_wl = sim.Queue("storage4")
presswaitingline = sim.Queue("presswaitingline")
cutwaitingline = sim.Queue("cutwaitingline")
finwaitingline = sim.Queue("finwaitingline")
paintwaitingline = sim.Queue("paintwaitingline")
packdeckwaitingline = sim.Queue("packdeckwaitingline")
packwheelswaitingline = sim.Queue("packwheelwaitingline")
assemblywaitingline = sim.Queue("assemblywaitingline")
foundrywaitingline = sim.Queue("foundrywaitingline")
machiningwaitingline = sim.Queue("machiningwaitingline")
printingwaitingline = sim.Queue("printingwaitingline")

Final = ["packingwheels","packingdecks", "assembly","assembly","assembly"]

env.run(till=31680) #22 dias

print()
presswaitingline.print_statistics()
cutwaitingline.print_statistics()
finwaitingline.print_statistics()
paintwaitingline.print_statistics()
foundrywaitingline.print_statistics()
machiningwaitingline.print_statistics()
printingwaitingline.print_statistics()
assemblywaitingline.print_statistics()
packdeckwaitingline.print_statistics()
packwheelswaitingline.print_statistics()
storage1_wl.print_statistics()
storage2_wl.print_statistics()
storage3_wl.print_statistics()
storage4_wl.print_statistics()
print("Skates:",skates)
print("Caixas de rodas:",Conjunto_rodas)
print("Caixas de pranchas:",Conjunto_pranchas)
        