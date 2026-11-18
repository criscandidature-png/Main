"""Bot Sistema: stato del PC, processi, spegnimento."""
import platform, subprocess, time
import psutil
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler
from pcbot.auth import restricted

IS_WIN = platform.system() == "Windows"


@restricted
async def status(update, context):
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\" if IS_WIN else "/")
    up = int(time.time() - psutil.boot_time()) // 60
    bat = psutil.sensors_battery()
    txt = (f"🖥 {platform.node()} ({platform.system()})\n"
           f"CPU: {cpu}%\nRAM: {mem.percent}% di {mem.total // 2**30} GB\n"
           f"Disco: {disk.percent}%\nAcceso da: {up // 60}h {up % 60}m")
    if bat:
        txt += f"\nBatteria: {bat.percent}%{' 🔌' if bat.power_plugged else ''}"
    await update.message.reply_text(txt)


@restricted
async def processes(update, context):
    procs = sorted(psutil.process_iter(["pid", "name", "memory_percent"]),
                   key=lambda p: p.info["memory_percent"] or 0, reverse=True)[:15]
    lines = [f"{p.info['pid']:>6} {p.info['memory_percent']:.1f}% {p.info['name']}" for p in procs]
    await update.message.reply_text("Top processi (RAM):\n<pre>" + "\n".join(lines) + "</pre>",
                                    parse_mode="HTML")


@restricted
async def kill(update, context):
    if not context.args:
        return await update.message.reply_text("Uso: /kill <pid o nome>")
    target, n = context.args[0], 0
    for p in psutil.process_iter(["pid", "name"]):
        if str(p.info["pid"]) == target or (p.info["name"] or "").lower() == target.lower():
            try:
                p.kill(); n += 1
            except psutil.Error:
                pass
    await update.message.reply_text(f"Terminati {n} processi.")


POWER = {
    "shutdown": ("Spegni", "shutdown /s /t 5" if IS_WIN else "shutdown -h now"),
    "restart": ("Riavvia", "shutdown /r /t 5" if IS_WIN else "shutdown -r now"),
    "lock": ("Blocca", "rundll32.exe user32.dll,LockWorkStation" if IS_WIN else "loginctl lock-session"),
    "sleep": ("Sospendi", "rundll32.exe powrprof.dll,SetSuspendState 0,1,0" if IS_WIN else "systemctl suspend"),
}


@restricted
async def power(update, context):
    kb = [[InlineKeyboardButton(label, callback_data=f"pw:{k}")] for k, (label, _) in POWER.items()]
    kb.append([InlineKeyboardButton("Annulla", callback_data="pw:cancel")])
    await update.message.reply_text("⚡ Cosa vuoi fare?", reply_markup=InlineKeyboardMarkup(kb))


@restricted
async def power_cb(update, context):
    q = update.callback_query
    await q.answer()
    key = q.data.split(":")[1]
    if key not in POWER:
        return await q.edit_message_text("Annullato.")
    await q.edit_message_text(f"✅ {POWER[key][0]}...")
    subprocess.Popen(POWER[key][1], shell=True)


HANDLERS = [CommandHandler("status", status), CommandHandler("processi", processes),
            CommandHandler("kill", kill), CommandHandler("power", power),
            CallbackQueryHandler(power_cb, pattern=r"^pw:")]
HELP = ("/status – stato del PC\n/processi – top processi\n/kill <pid|nome>\n"
        "/power – spegni/riavvia/blocca/sospendi")
