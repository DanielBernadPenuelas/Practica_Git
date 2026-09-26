#  Hijoputismo proyect

> [!CAUTION]
> **Este repositorio está hecho para ser destruido.**
> **Esta hecho para practicar el hijoputismo**
> Todo lo que se suba aquí puede ser borrado, sobrescrito o perdido en cualquier momento, sin aviso.
> **Si quieres hacer algo de valor, hazlo en tu propia cuenta.** No guardes aquí código, apuntes ni trabajos que te importen.

---

## ¿De qué va esto?

Este repositorio es un campo de entrenamiento para practicar Git en situaciones reales de caos.

El juego tiene dos bandos:

| Rol | Quién | Objetivo |
|-----|-------|----------|
| **Atacantes** | Mis compañeros | Romper el repositorio de todas las formas creativas posibles |
| **Restaurador** | Yo (propietario del repo) | Devolver el repositorio a un estado sano, recuperar lo destruido y proteger lo importante |

La idea es aprender, de forma práctica, a:

- Recuperar archivos, commits y ramas borradas.
- Deshacer historiales reescritos y `force push`.
- Resolver conflictos de merge.
- Bloquear y desbloquear archivos (Git LFS file locking y protección de ramas).
- Entender qué se puede recuperar y qué no.

---

## Aviso importante

- **Nada de lo que hay aquí es permanente.** Da por hecho que cualquier archivo puede desaparecer.
- **No uses este repositorio como copia de seguridad** ni como sitio para tu trabajo real.
- **Si quieres construir algo útil, crea un repositorio en tu cuenta** o haz un fork y trabaja allí.
- El propietario no se responsabiliza de nada que se pierda en este repositorio. Ese es literalmente el objetivo.

---

## Reglas para los atacantes

###  Se permite (y se anima)

- Borrar archivos y carpetas.
- Modificar o corromper el contenido de los archivos.
- Renombrar y mover todo de sitio.
- Crear conflictos a propósito en ramas distintas.
- Borrar ramas (incluida `main`, si los permisos lo dejan).
- Reescribir el historial (`rebase`, `reset`, `commit --amend`) y hacer `git push --force`.
- Bloquear archivos con `git lfs lock` para ponerle las cosas difíciles al restaurador.
- Hacer commits con mensajes absurdos o engañosos.
- Combinar varios ataques a la vez.

###  No se permite

- Subir contraseñas, tokens, claves o cualquier dato sensible (ni tuyo ni de nadie).
- Subir datos personales de otras personas.
- Subir malware, scripts maliciosos o cualquier cosa que pueda dañar el equipo de quien clone el repo.
- Contenido ofensivo, ilegal o que pueda meter a alguien en problemas.
- Archivos gigantes que agoten la cuota del repositorio.
- Atacar cuentas, repositorios o servicios que no sean **este** repositorio.

> El objetivo es aprender Git, no hacer daño de verdad. Se rompe el repositorio, no a las personas.

---

## 🛠️ Chuleta del restaurador

### Recuperar archivos borrados o modificados

```bash
# Ver qué ha cambiado
git status
git log --stat

# Restaurar un archivo desde el último commit
git restore ruta/al/archivo

# Restaurar un archivo desde un commit concreto
git restore --source=<hash> ruta/al/archivo

# Encontrar el commit en el que se borró un archivo
git log --diff-filter=D -- ruta/al/archivo
```

### Deshacer commits

```bash
# Deshacer un commit creando otro que lo revierte (seguro en ramas compartidas)
git revert <hash>

# Volver a un estado anterior (reescribe historial, ¡cuidado!)
git reset --hard <hash>
```

### Recuperar lo "irrecuperable"

```bash
# El reflog guarda por dónde ha pasado HEAD, aunque el historial se haya reescrito
git reflog

# Volver a un punto del reflog
git reset --hard HEAD@{n}

# Recuperar una rama borrada
git branch nombre-rama <hash>

# Buscar commits huérfanos
git fsck --lost-found
```

>  El `reflog` es local: solo funciona en un clon que haya visto esos commits. Mantén siempre un clon tuyo actualizado; es tu mejor seguro.

### Arreglar un force push de otra persona

```bash
git fetch origin
git reflog                          # busca el estado bueno en tu clon local
git reset --hard <hash-bueno>
git push --force-with-lease origin main
```

### Bloquear y desbloquear archivos (Git LFS)

```bash
# Instalar y activar LFS en el repo
git lfs install
git lfs track "*.bin" --lockable

# Ver qué archivos están bloqueados y por quién
git lfs locks

# Bloquear un archivo
git lfs lock ruta/al/archivo

# Desbloquear un archivo propio
git lfs unlock ruta/al/archivo

# Forzar el desbloqueo de un archivo de otra persona (requiere permisos de administrador)
git lfs unlock ruta/al/archivo --force
```

### Proteger ramas

Desde la configuración del repositorio en GitHub (**Settings → Branches / Rules**) el propietario puede:

- Impedir `force push` en `main`.
- Impedir que se borre la rama.
- Obligar a pasar por Pull Request antes de fusionar.

Activar y desactivar estas protecciones también forma parte del juego: se pueden quitar para dejar vía libre a los ataques y volver a ponerlas para practicar la defensa.

---

## Registro de rondas

Para que la práctica sirva de algo, apuntamos qué se rompió y cómo se arregló.

| Ronda | Atacante | Qué rompió | Cómo se restauró | ¿Recuperado? |
|-------|----------|------------|------------------|--------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

---

## Cómo participar

1. Pide al propietario que te añada como colaborador.
2. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   ```
3. Rompe cosas respetando las reglas.
4. Avisa cuando termines tu ataque (o no, y que el restaurador lo descubra).

---

## Recordatorio final

**Este repositorio es un campo de pruebas, no un lugar para guardar nada.**
**Si algo te importa, súbelo a tu propia cuenta.** 🙂
