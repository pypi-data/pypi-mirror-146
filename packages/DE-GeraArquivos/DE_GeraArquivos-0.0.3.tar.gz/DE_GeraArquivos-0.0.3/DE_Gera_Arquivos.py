import datetime as dt
import pandas as pd
import inspect
import os
import csv
import json
import pandavro as pdx


class ARQUIVOS():
    def __init__(self, **kwargs):
        self._valida_kwargs(**kwargs)
        pass

    def _valida_kwargs(self, **kwargs):
        global gPROCESSO, gDF, gFILE, gEXT, gPATH, gSUFIX, gINDEX, gLOG, gLOGGER, gPAYLOAD, gFILE_TYPE, FILE_STATUS
        gPROCESSO, gDF, gFILE, gEXT, gPATH, gSUFIX, gINDEX, gLOG, gLOGGER, gPAYLOAD, gFILE_TYPE, FILE_STATUS, msg = \
            None, None, None, None, None, None, None, None, None, None, None, None, None
        msg = None
        try:
            gFILE_TYPE = {"PARQUET": "parquet", "CSV": "csv", "JSON": "json", "TXT": "txt", "ZIP": "zip", "XLSX": "xlsx", "AVRO": "avro"}
            if "processo" in kwargs.keys():
                gPROCESSO = kwargs.get("processo")
            if "dataframe" in kwargs.keys():
                gDF = kwargs.get("dataframe")
            if "file_name" in kwargs.keys():
                gFILE = kwargs.get("file_name")
            if "ext_list" in kwargs.keys():
                gEXT = kwargs.get("ext_list")
            if "file_path" in kwargs.keys():
                gPATH = kwargs.get("file_path")
            if "file_sufix" in kwargs.keys():
                gSUFIX = kwargs.get("file_sufix")
            if "index" in kwargs.keys():
                gINDEX = kwargs.get("index")
            if "log" in kwargs.keys():
                gLOG = kwargs.get("log")
            if "logger" in kwargs.keys():
                gLOGGER = kwargs.get("logger")
            if "payload" in kwargs.keys():
                gPAYLOAD = kwargs.get("payload")
            msg = "kwargs validados!"

        except Exception as error:
            msg = error
        finally:

            return msg

    def TXT(self,
            df: pd.DataFrame,
            file_name: str,
            file_sufix: str = "",
            file_path: str = "",
            sep: str = "\t",
            na_rep: str = "",
            float_format: str = None,
            columns: list = None,
            header: bool = True,
            index: bool = True,
            index_label: str = None,
            mode: str = 'w',
            encoding: str = None,
            compression: str = "infer",
            quoting: int = csv.QUOTE_ALL,
            quotechar: str = "\"",
            line_terminator: str = None,
            chunksize=None,
            date_format: str = "%Y-%m-%d %H:%M:%S",
            doublequote: bool = True,
            escapechar: str = None,
            decimal: str = ".",
            errors: str = "strict",
            storage_options: str = None
            ):
        msg, size, ext_inicio, ext_termino, ext_tempo = None, None, None, None, None
        function_name = inspect.stack()[0].function
        extensao = gFILE_TYPE["TXT"]
        ext_inicio = dt.datetime.now()
        file_name = f"""{file_name}{file_sufix}.{extensao}"""
        full_filename = os.path.join(file_path, file_name)
        if isinstance(gLOG, object):
            msg = f"""Iniciando extração para o arquivo {file_name}"""
            gLOG.Popula(logger=gLOGGER, level=gLOG.INFO, content=msg, function_name=function_name, cor=gLOG.Italico, lf=False)
        try:
            df.to_csv(path_or_buf=full_filename,
                      sep=sep,
                      na_rep=na_rep,
                      float_format=float_format,
                      columns=columns,
                      header=header,
                      index=index,
                      index_label=index_label,
                      mode=mode,
                      encoding=encoding,
                      compression=compression,
                      quoting=quoting,
                      quotechar=quotechar,
                      line_terminator=line_terminator,
                      chunksize=chunksize,
                      date_format=date_format,
                      doublequote=doublequote,
                      escapechar=escapechar,
                      decimal=decimal,
                      errors=errors,
                      storage_options=storage_options)
            msg = "Arquivo gerado com sucesso!"
            size = os.path.getsize(full_filename)
            loginfo = gLOG.INFO
        except Exception as error:
            msg = error
            loginfo = gLOG.ERROR
        finally:
            ext_termino = dt.datetime.now()
            ext_tempo = ext_termino - ext_inicio
            status = {"filename": full_filename, "size": size, "ext_inicio": str(ext_inicio), "ext_termino": str(ext_termino), "ext_tempo": str(ext_tempo), "msg": msg}
            if isinstance(gLOG, object):
                gLOG.Popula(logger=gLOGGER, level=loginfo, content=msg, function_name=function_name, cor=gLOG.Italico)
            return status

    def CSV(self,
            df: pd.DataFrame,
            file_name: str,
            file_sufix: str = None,
            file_path: str = "",
            sep: str = ";",
            na_rep: str = "",
            float_format: str = None,
            columns: list = None,
            header: bool = True,
            index: bool = True,
            index_label: str = None,
            mode: str ='w',
            encoding: str = None,
            compression: str = "infer",
            quoting: int = csv.QUOTE_ALL,
            quotechar: str = "\"",
            line_terminator: str = None,
            chunksize=None,
            date_format: str = "%Y-%m-%d %H:%M:%S",
            doublequote: bool = True,
            escapechar: str = None,
            decimal: str = ".",
            errors: str = "strict",
            storage_options: str = None
            ):
        msg, size, ext_inicio, ext_termino, ext_tempo = None, None, None, None, None
        function_name = inspect.stack()[0].function
        extensao = gFILE_TYPE["CSV"]
        ext_inicio = dt.datetime.now()
        file_name = f"""{file_name}{file_sufix}.{extensao}"""
        full_filename = os.path.join(file_path, file_name)
        if isinstance(gLOG, object):
            msg = f"""Iniciando extração para o arquivo {file_name}"""
            gLOG.Popula(logger=gLOGGER, level=gLOG.INFO, content=msg, function_name=function_name, cor=gLOG.Italico, lf=False)
        try:
            df.to_csv(path_or_buf=full_filename,
                      sep=sep,
                      na_rep=na_rep,
                      float_format=float_format,
                      columns=columns,
                      header=header,
                      index=index,
                      index_label=index_label,
                      mode=mode,
                      encoding=encoding,
                      compression=compression,
                      quoting=quoting,
                      quotechar=quotechar,
                      line_terminator=line_terminator,
                      chunksize=chunksize,
                      date_format=date_format,
                      doublequote=doublequote,
                      escapechar=escapechar,
                      decimal=decimal,
                      errors=errors,
                      storage_options=storage_options)
            msg = "Arquivo gerado com sucesso!"
            size = os.path.getsize(full_filename)
            loginfo = gLOG.INFO
        except Exception as error:
            msg = error
            loginfo = gLOG.ERROR
        finally:
            ext_termino = dt.datetime.now()
            ext_tempo = ext_termino - ext_inicio
            status = {"filename": full_filename, "size": size, "ext_inicio": str(ext_inicio), "ext_termino": str(ext_termino),
                      "ext_tempo": str(ext_tempo), "msg": msg}
            if isinstance(gLOG, object):
                gLOG.Popula(logger=gLOGGER, level=loginfo, content=msg, function_name=function_name, cor=gLOG.Italico)
            return status

    def XLSX(self,
             df: pd.DataFrame,
             file_name: str,
             file_path: str = "",
             file_sufix: str = "",
             sheet_name: str = 'Dados',
             na_rep: str = "",
             float_format: str = None,
             columns: list = None,
             header: bool = True,
             index: bool = True,
             index_label=None,
             startrow: int = 0,
             startcol: int = 0,
             engine: str = "xlsxwriter",
             merge_cells=True,
             encoding: str =None,
             inf_rep: str = "inf",
             verbose: bool = True,
             freeze_panes=None,
             storage_options=None
             ):
        msg, size, ext_inicio, ext_termino, ext_tempo = None, None, None, None, None
        function_name = inspect.stack()[0].function
        extensao = gFILE_TYPE["XLSX"]
        ext_inicio = dt.datetime.now()
        file_name = f"""{file_name}{file_sufix}.{extensao}"""
        full_filename = os.path.join(file_path, file_name)
        if isinstance(gLOG, object):
            msg = f"""Iniciando extração para o arquivo {file_name}"""
            gLOG.Popula(logger=gLOGGER, level=gLOG.INFO, content=msg, function_name=function_name, cor=gLOG.Italico, lf=False)
        try:
            df.to_excel(full_filename,
                        sheet_name=sheet_name,
                        na_rep=na_rep,
                        float_format=float_format,
                        columns=columns,
                        header=header,
                        index=index,
                        index_label=index_label,
                        startrow=startrow,
                        startcol=startcol,
                        engine=engine,
                        merge_cells=merge_cells,
                        encoding=encoding,
                        inf_rep=inf_rep,
                        verbose=verbose,
                        freeze_panes=freeze_panes,
                        storage_options=storage_options)
            msg = "Arquivo gerado com sucesso!"
            size = os.path.getsize(full_filename)
            loginfo = gLOG.INFO
        except Exception as error:
            msg = error
            loginfo = gLOG.ERROR
        finally:
            ext_termino = dt.datetime.now()
            ext_tempo = ext_termino - ext_inicio
            status = {"filename": full_filename, "size": size, "ext_inicio": str(ext_inicio), "ext_termino": str(ext_termino),
                      "ext_tempo": str(ext_tempo), "msg": msg}
            if isinstance(gLOG, object):
                gLOG.Popula(logger=gLOGGER, level=loginfo, content=msg, function_name=function_name, cor=gLOG.Italico)
            return status

    def PARQUET(self,
                df: pd.DataFrame,
                file_name: str,
                file_sufix: str = None,
                file_path: str = "",
                engine: str = "pyarrow",
                compression: str = "snappy",
                index: bool = False,
                partition_cols=None
                ):
        msg, size, ext_inicio, ext_termino, ext_tempo = None, None, None, None, None
        function_name = inspect.stack()[0].function
        extensao = gFILE_TYPE["PARQUET"]
        ext_inicio = dt.datetime.now()
        file_name = f"""{file_name}{file_sufix}.{extensao}"""
        full_filename = os.path.join(file_path, file_name)
        if isinstance(gLOG, object):
            msg = f"""Iniciando extração para o arquivo {file_name}"""
            gLOG.Popula(logger=gLOGGER, level=gLOG.INFO, content=msg, function_name=function_name, cor=gLOG.Italico, lf=False)
        try:
            df.to_parquet(path=full_filename,
                          engine=engine,
                          compression=compression,
                          index=index,
                          partition_cols=partition_cols
                          )
            msg = "Arquivo gerado com sucesso!"
            size = os.path.getsize(full_filename)
            loginfo = gLOG.INFO
        except Exception as error:
            msg = error
            loginfo = gLOG.ERROR
        finally:
            ext_termino = dt.datetime.now()
            ext_tempo = ext_termino - ext_inicio
            status = {"filename": full_filename, "size": size, "ext_inicio": str(ext_inicio), "ext_termino": str(ext_termino),
                      "ext_tempo": str(ext_tempo), "msg": msg}
            if isinstance(gLOG, object):
                gLOG.Popula(logger=gLOGGER, level=loginfo, content=msg, function_name=function_name, cor=gLOG.Italico)
            return status

    def JSON(self,
             df: pd.DataFrame,
             file_name: str,
             file_sufix: str = None,
             file_path: str = "",
             orient: str = "records",
             date_format: str =None,
             double_precision: int = 10,
             force_ascii: bool = True,
             date_unit: str = 'ms',
             default_handler=None,
             lines: bool = False,
             compression: str = "infer",
             index: bool = True,
             indent: int = 2,
             storage_options=None,
             payload: dict = None
             ):
        msg, size, ext_inicio, ext_termino, ext_tempo = None, None, None, None, None
        function_name = inspect.stack()[0].function
        extensao = gFILE_TYPE["JSON"]
        ext_inicio = dt.datetime.now()
        file_name = f"""{file_name}{file_sufix}.{extensao}"""
        full_filename = os.path.join(file_path, file_name)
        if isinstance(gLOG, object):
            msg = f"""Iniciando extração para o arquivo {file_name}"""
            gLOG.Popula(logger=gLOGGER, level=gLOG.INFO, content=msg, function_name=function_name, cor=gLOG.Italico, lf=False)
        try:
            if payload is not None:
                with open(full_filename, "w", encoding='utf-8') as outfile:
                    json.dump(payload, outfile, indent=2)
            else:
                if orient not in ["split", "table"]:
                    df.to_json(path_or_buf=full_filename,
                               orient=orient,
                               date_format=date_format,
                               double_precision=10,
                               force_ascii=force_ascii,
                               date_unit=date_unit,
                               default_handler=default_handler,
                               lines=lines,
                               compression=compression,
                               #index=index,
                               indent=indent,
                               storage_options=storage_options)
                else:
                    df.to_json(path_or_buf=full_filename,
                               orient=orient,
                               date_format=date_format,
                               double_precision=10,
                               force_ascii=force_ascii,
                               date_unit=date_unit,
                               default_handler=default_handler,
                               lines=lines,
                               compression=compression,
                               index=index,
                               indent=indent,
                               storage_options=storage_options)
            msg = "Arquivo gerado com sucesso!"
            size = os.path.getsize(full_filename)
            loginfo = gLOG.INFO
        except Exception as error:
            msg = error
            loginfo = gLOG.ERROR
        finally:
            ext_termino = dt.datetime.now()
            ext_tempo = ext_termino - ext_inicio
            status = {"filename": full_filename, "size": size, "ext_inicio": str(ext_inicio), "ext_termino": str(ext_termino),
                      "ext_tempo": str(ext_tempo), "msg": msg}
            if isinstance(gLOG, object):
                gLOG.Popula(logger=gLOGGER, level=loginfo, content=msg, function_name=function_name, cor=gLOG.Italico)
            return status

    def JSON_DL(self,
                 payload: dict,
                 file_name: str,
                 file_sufix: str = None,
                 file_path: str = "",
                 orient: str = "records",
                 date_format: str =None,
                 double_precision: int = 10,
                 force_ascii: bool = True,
                 date_unit: str = 'ms',
                 default_handler=None,
                 lines: bool = False,
                 compression: str = "infer",
                 index: bool = True,
                 indent: bool = False,
                 storage_options=None):
        msg, size, ext_inicio, ext_termino, ext_tempo = None, None, None, None, None
        function_name = inspect.stack()[0].function
        extensao = gFILE_TYPE["JSON"]
        ext_inicio = dt.datetime.now()
        file_name = f"""{file_name}{file_sufix}.{extensao}"""
        full_filename = os.path.join(file_path, file_name)
        if isinstance(gLOG, object):
            msg = f"""Iniciando extração para o arquivo {file_name}"""
            gLOG.Popula(logger=gLOGGER, level=gLOG.INFO, content=msg, function_name=function_name, cor=gLOG.Italico, lf=False)
        try:
            with open(full_filename, "w", encoding='utf-8') as outfile:
                json.dump(payload, outfile, indent=2)
            msg = "Arquivo gerado com sucesso!"
            size = os.path.getsize(full_filename)
            loginfo = gLOG.INFO
        except Exception as error:
            msg = error
            loginfo = gLOG.ERROR
        finally:
            ext_termino = dt.datetime.now()
            ext_tempo = ext_termino - ext_inicio
            status = {"filename": full_filename, "size": size, "ext_inicio": str(ext_inicio), "ext_termino": str(ext_termino),
                      "ext_tempo": str(ext_tempo), "msg": msg}
            if isinstance(gLOG, object):
                gLOG.Popula(logger=gLOGGER, level=loginfo, content=msg, function_name=function_name, cor=gLOG.Italico)
            return status

    def AVRO(self,
             df: pd.DataFrame,
             file_name: str,
             file_sufix: str = "",
             file_path: str = ""
             ):
        msg, size, ext_inicio, ext_termino, ext_tempo = None, None, None, None, None
        function_name = inspect.stack()[0].function
        extensao = gFILE_TYPE["AVRO"]
        ext_inicio = dt.datetime.now()
        file_name = f"""{file_name}{file_sufix}.{extensao}"""
        full_filename = os.path.join(file_path, file_name)
        try:
            pdx.to_avro(file_path_or_buffer=full_filename, df=df)
            size = os.path.getsize(full_filename)
            tipolog = self._log.INFO
            msg = "Arquivo gerado com sucesso!"
            size = os.path.getsize(full_filename)
            loginfo = gLOG.INFO
        except Exception as error:
            msg = error
            loginfo = gLOG.ERROR
        finally:
            ext_termino = dt.datetime.now()
            ext_tempo = ext_termino - ext_inicio
            status = {"filename": full_filename, "size": size, "ext_inicio": str(ext_inicio), "ext_termino": str(ext_termino),
                      "ext_tempo": str(ext_tempo), "msg": msg}
            if isinstance(gLOG, object):
                gLOG.Popula(logger=gLOGGER, level=loginfo, content=msg, function_name=function_name, cor=gLOG.Italico)
            return status