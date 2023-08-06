#!/usr/bin/env python

from pycomando import Comando
import logging, sys, pprint

def main():
    comando = Comando(yml='args.yml')

    parser = comando.get_parser()
    arguments_dict = vars(parser.parse_args())
    log_level = arguments_dict.get("log_level", None)
    print(f'log_level: {log_level}')
    comando.setup_logging(log_level)
    arguments_dict.pop("log_level", None)
    comando = arguments_dict.pop("subcommand")

    if comando == 'subcomando':
        print('Comando ejecutado exitosamente, se detecto el subcomando:')
        #print(f'Run {comando} with **arguments_dict: {arguments_dict}')
        pprint.pprint(arguments_dict)
    sys.exit(0)

if __name__ == "__main__":
    main()