import tkinter as tk

class MapaAutobus:
    def __init__(self):
        self.mapa = self.leer_mapa('/home/beto/Documents/GitHub/Practica_2_Heuristica/parte-2/ASTAR-tests/17_normal.csv')
        self.ruta = self.leer_ruta('/home/beto/Documents/GitHub/Practica_2_Heuristica/parte-2/ASTAR-tests/17_normal-1.output')
        self.current_step = 0
        self.contador_N = 0
        self.contador_C = 0
        self.casillas_contadas_N = set()
        self.casillas_contadas_C = set()

        self.root = tk.Tk()
        self.root.title("Ruta del Autobús")

        self.canvas = tk.Canvas(self.root, width=50 * len(self.mapa[0]), height=50 * len(self.mapa))
        self.canvas.pack()

        self.avanzar_btn = tk.Button(self.root, text="Avanzar", command=self.avanzar)
        self.avanzar_btn.pack(side=tk.LEFT, padx=10)

        self.resetear_btn = tk.Button(self.root, text="Resetear", command=self.resetear_mapa)
        self.resetear_btn.pack(side=tk.LEFT, padx=10)

        self.energia_label = tk.Label(self.root, text="Energía restante: ")
        self.energia_label.pack()

        self.contador_N_label = tk.Label(self.root, text="Pacientes N en el bus: 0")
        self.contador_N_label.pack()

        self.contador_C_label = tk.Label(self.root, text="Pacientes C en el bus: 0")
        self.contador_C_label.pack()

        self.dibujar_mapa()

        self.root.mainloop()

    def leer_mapa(self, file):
        with open(file, 'r') as f:
            mapa = [line.strip().split(';') for line in f.readlines()]
        return mapa

    def leer_ruta(self, file):
        with open(file, 'r') as f:
            ruta = [line.strip().split(':') for line in f.readlines()]
        return ruta

    def dibujar_mapa(self):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[0])):
                if self.mapa[i][j] != 'X':
                    if self.mapa[i][j] == 'CC':
                        self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill='#a0acde', outline='black')
                    elif self.mapa[i][j] == 'CN':
                        self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill='#e0aeeb', outline='black')
                    elif self.mapa[i][j] == 'C':
                        self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill='#6776b8', outline='black')
                    elif self.mapa[i][j] == 'N':
                        self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill='#a266b0', outline='black')
                    else:
                        self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill='#adadad', outline='black')
                    self.canvas.create_text(j * 50 + 25, i * 50 + 25, text=self.mapa[i][j])

    def resetear_mapa(self):
        self.canvas.delete("autobus")
        self.current_step = 0
        self.contador_N = 0
        self.contador_C = 0
        self.casillas_contadas_N = set()
        self.casillas_contadas_C = set()
        self.contador_N_label.config(text=f"Pacientes N en el bus: {self.contador_N}")
        self.contador_C_label.config(text=f"Pacientes C en el bus: {self.contador_C}")

        # reseteamos el canvas
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[0])):
                if self.mapa[i][j] != 'X':
                    if self.mapa[i][j] == 'CC':
                        self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill='#a0acde', outline='black')
                    elif self.mapa[i][j] == 'CN':
                        self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill='#e0aeeb', outline='black')
                    elif self.mapa[i][j] == 'C':
                        self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill='#6776b8', outline='black')
                    elif self.mapa[i][j] == 'N':
                        self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill='#a266b0', outline='black')
                    else:
                        self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill='#adadad', outline='black')
                    self.canvas.create_text(j * 50 + 25, i * 50 + 25, text=self.mapa[i][j])

    def actualizar_energia(self):
        energia = int(self.ruta[self.current_step][2])
        self.energia_label.config(text=f"Energía restante: {energia}")

    def actualizar_contadores(self):
        tipo_casilla = self.ruta[self.current_step][1]
        if tipo_casilla == 'N' and self.ruta[self.current_step][0] not in self.casillas_contadas_N \
            and self.contador_C == 0 and (self.contador_C + self.contador_N) < 10:
            self.contador_N += 1
            self.casillas_contadas_N.add(self.ruta[self.current_step][0])
            self.contador_N_label.config(text=f"Pacientes N en el bus: {self.contador_N}")
        elif tipo_casilla == 'CN' and self.contador_C == 0:
            self.contador_N = 0
            self.contador_N_label.config(text=f"Pacientes N en el bus: {self.contador_N}")
        if tipo_casilla == 'C' and self.ruta[self.current_step][0] not in self.casillas_contadas_C \
            and self.contador_N <= 8 and self.contador_C < 2:
            self.contador_C += 1
            self.casillas_contadas_C.add(self.ruta[self.current_step][0])
            self.contador_C_label.config(text=f"Pacientes C en el bus: {self.contador_C}")
        elif tipo_casilla == 'CC':
            self.contador_C = 0
            self.contador_C_label.config(text=f"Pacientes C en el bus: {self.contador_C}")

    def avanzar(self):
        if self.current_step < len(self.ruta):
            self.dibujar_paso(self.current_step)
            self.actualizar_energia()
            self.actualizar_contadores()
            self.current_step += 1

    def retroceder(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.dibujar_paso(self.current_step, clear=True)
            self.actualizar_energia()
            self.actualizar_contadores()

    def dibujar_paso(self, step, clear=False):
        if clear:
            self.canvas.delete("autobus")
        for i in range(step + 1):
            coord = self.ruta[i][0].replace('(', '').replace(')', '').split(', ')
            x, y = int(coord[0]) - 1, int(coord[1]) - 1
            if i == step:
                self.canvas.create_oval(y * 50 + 10, x * 50 + 10, (y + 1) * 50 - 10, (x + 1) * 50 - 10, fill='#e89e99', tags="autobus")
                self.canvas.create_text(y * 50 + 25, x * 50 + 25, text=self.ruta[i][1], tags="autobus")
            else:
                self.canvas.create_oval(y * 50 + 10, x * 50 + 10, (y + 1) * 50 - 10, (x + 1) * 50 - 10, fill='#92d4c4')
                self.canvas.create_text(y * 50 + 25, x * 50 + 25, text=self.ruta[i][1], tags="autobus")

MapaAutobus()
