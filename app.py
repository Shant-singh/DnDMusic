from flask import Flask
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from functools import wraps

from models import db

app = Flask(__name__)
app.secret_key = 'nVTnu_Y8tEZ9h1Z5sLKSMWXMgG_781x1jr4jqu2qWlYm9SOB0Ff3xXyXYS_Xqc5IJTfnkdz4tSETqodVrmJAy7cAf3JtcpjYT0Cl4IQ29tnA5TEpPg4DiQYrUTYWVFeSo_N_gnFbtZQzZKZWeSeuku5rGUtj_YA6XJKxcs4ZQrd5fy6gNvFBcMiVrPAhxI2thdi5Um3IrCHJITr7kacKUPbcn_Otb4hDNRltyVGtmOJnGNwM_vGApQF7VrjoO_y0yJFe6jepfYEOayeCKustjoLvqBh4nbELsit06r_340kfLQQ0yJKcGNUU10xmuwNn79NC9MSjG7GPfDsiRV1PkIMoPmnOI8YI5FDXK2ejTxSY6jVpCphvEYYUnShR7m9FfLwVFU37zNRLtcfCW5ef942OxYtdEpcm5iUKt2TkwIOyjRtJDEciqlSaM15ziNhPh3bXVmsPjPUiETxBar9DGlb0TVVeoUV54FWkuU2LREMPKHSP2Gm4tgTyu7VpLPdschdoTCavLGZqvHA6IZaJBrOAQUd0tEW7qAHWG6CIKh68vyjWm9kaqPOIp3BijGXTmn_FhUZ7uoQk_mgv96Fu2uNaMM9pazumL0tOZ5LdvfrihUCYTKmjEsiYXWS_3ksriGhPn_bqibnfdcPMiRvagpmSN9njfOCB8ijluD_hc3FSGTKn4A_xtcDLS9BGyXdp4ysSldllTZXa0IbKd4EBWLnLGhoXsWOP8oMxY_vBnmpANlcfadTdAPJzlup1T2rizzmV6sQvZYcRzKR8xtWqJ65NhvwxpiMJV80n4jE6fx15YEJaDk9eIQJcCcOtV25rgxqCJBYIMldn7uSr1aC0ntBrl_bJXMlyZOJ3XP6zRayR7f8KI89JgT3U2un0kdQi5oMn0EdXr1phYeJhVO7u3xMYHscNtuQ48wV7h2XsSrL8W3e0pFFde6VMQcgoIw42wu5HzoY6tgIIy8bIBecKztu966SxxRfCmTnIv_Ddksl4vial_lNaFDENlYUTYD8p'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app=app)
migrate = Migrate(app, db)

db.create_all(app=app)

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)