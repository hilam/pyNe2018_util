# ler programaçção de um csv e montar trecho de código html
# para injetar na página
import csv

generated = open("generated.txt","w+")

with open("programacao.csv") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        target = row["Alias"]
        if not target:
            continue
        titulo = row["Título"]
        nome = row["Palestrante"]
        email = row["E-mail"]
        imagem = row["Foto"]
        bio = row["Bio"]

        trecho = f"""
                          <button type="button" class="btn btn-link" data-toggle="modal" data-target="#{target}">
                            {titulo}
                          </button>
    
                          <!-- Modal -->
                          <div class="modal fade" id="{target}" tabindex="-1" role="dialog" aria-labelledby="{target}Title" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered" role="document">
                              <div class="modal-content">
                                <div class="modal-header">
                                  <h5 class="modal-title" id="{target}LongTitle">Apresentação</h5>
                                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                  </button>
                                </div>
                                <div class="modal-body">
                                  <img src="img/palestrantes/{imagem}" class="rounded mx-auto d-block" alt="avatar palestrante" width="80px">
                                  <br>
                                  <h4>{nome}</h4>
                                  <p>
                                    {bio}
                                  </p>
                                  <div class="container">
                                    <p class="text-left">
                                      <i class="material-icons align-middle">email</i>
                                      {email}
                                    </p>
                                  </div>
                                </div>
                                <div class="modal-footer">
                                  <button type="button" class="btn btn-secondary" data-dismiss="modal">Fechar</button>
                                </div>
                              </div>
                            </div>
                          </div>
        """
        generated.write(f"Palestra: {titulo}\r\n")
        generated.write(f"{trecho}\r\n\n")

generated.close()
