
from oslo_config import cfg


CONFIG_OPTS = [
    cfg.StrOpt("consumer",
               default="file",
               help="Consumer implementation to process operation "
                    "records. One of 'file', 'nop'"),
    cfg.StrOpt("data-dir",
               default="/var/spool/oslo.devsupport",
               metavar="data_dir",
               help="Directory in which to save operation records when "
                     "using file based consumer"),
    cfg.BoolOpt("enabled",
                default=False,
                help="Whether processing of operation records is "
                     "initially enabled at startup"),
    cfg.BoolOpt("callstack",
                default=False,
                help="Whether to record call stack for each operation."),
]


def register(conf):
    conf.register_opts(CONFIG_OPTS,
                       group="devsupport")
