# -*- coding: utf-8 -*-
# Copyright (c) 2006-2010, Jesse Liesch
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE IMPLIED
# DISCLAIMED. IN NO EVENT SHALL JESSE LIESCH BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Modified by Jeramy Brian 9 - 17 - 13


import threading
import MySQLdb


class Db:
    def __init__(self, host, user, password, db, logger=None):
        self.name = db
        self.host = host
        self.user = user
        self.password = password

        self.logger = logger
        self.conns = {}
        self.connParams = {}
        self.transactionDepth = 0
        self.lastQuery = False

    def close(self):
        self.getConn().close()

    def getConnParam(self):
        threadId = threading.currentThread().getName()
        # Make sure we have a connection
        if not threadId in self.conns:
            self.getConn()
        return self.connParams[threadId]

    def getConn(self):
        # Return connection for current thread
        threadId = threading.currentThread().getName()
        if not threadId in self.conns:
            conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.name)
            self.connParams[threadId] = "?"
            self.conns[threadId] = conn
        return self.conns[threadId]

    def checkTable(self, name, fields, index=[], unique=[], engine=""):
        # Only allow one thread to check a table at a time
        # Otherwise we may have two threads create/update the same table

        # First create empty table
        try:
            createString = "create table if not exists " + name + "("
            first = True
            for f in fields:
                if first:
                    first = False
                else:
                    createString += ", "
                createString += f["name"] + " " + f["type"]
            createString += ")"
            if engine != "":
                createString += "ENGINE=" + engine
            curr = self.getConn().cursor()
            curr.execute(createString)
            curr.close()
        except Exception as e:
            if self.logger is not None:
                self.logger.log(e, "Warning")

        metaCurr = self.getConn().cursor()
        metaCurr.execute('show columns from ' + name)
        meta = metaCurr.fetchall()
        metaCurr.close()

        columns = []
        for c in meta:
            columns.append(c[0])
        meta = columns

        # Check for new fields
        for i in range(len(fields)):
            f = fields[i]
            found = False
            for m in meta:
                if f["name"] == m:
                    found = True
                    break
            if not found:
                # Create field
                alterString = "alter table " + name + " add " + f["name"] + " " + f["type"]
                curr = self.getConn().cursor()
                curr.execute(alterString)
                curr.close()

        indexCurr = self.getConn().cursor()
        indexCurr.execute('show index from ' + name)
        dbIndex = indexCurr.fetchall()
        indexCurr.close()

        indices = []
        first = True
        for i in dbIndex:
            if first:
                first = False
            else:
                indices.append(i[4])
        dbIndex = indices

        # Build index
        for j in range(len(index)):
            i = index[j]
            found = False
            for k in dbIndex:
                if i == k:
                    found = True
                    break
            if not found:
                # Create index
                alterString = "ALTER TABLE " + name + " ADD INDEX (" + i + ")"
                curr = self.getConn().cursor()
                curr.execute(alterString)
                curr.close()

        # Build unique index -- broken for now, don't currently need it'
        for i in unique:
            s = "create unique index if not exists " + i["name"] + " on " + name + "("
            first = True
            for col in i["cols"]:
                if first:
                    first = False
                else:
                    s += ", "

                s += col
            s += ")"

            curr = self.getConn().cursor()
            curr.execute(s)
            curr.close()

    def query(self, queryStr, tuple=False, reRaiseException=False, getRowCount=False):
        reRaiseException = True
        try:
            if tuple:
                self.lastQuery = "%s %s" % (queryStr, tuple)
                newQuery = queryStr + tuple
                curr = self.getConn().cursor()
                curr.execute(newQuery)
                result = curr.fetchall()
                curr.close()
                return result
            else:
                self.lastQuery = queryStr
                curr = self.getConn().cursor()
                curr.execute(queryStr)
                if getRowCount:
                    rowCount = curr.rowcount
                result = curr.fetchall()
                curr.close()
                if getRowCount:
                    return rowCount, result
                return result
        except Exception as e:
            if self.logger is not None:
                self.logger.log(e, "WARNING")
                return "Error"

            if reRaiseException:
                raise

            # Return empty string
            curr = self.getConn().cursor()
            curr.execute("select 0 where 1 = 0")
            result = curr.fetchone()
            curr.close()
            # Come back to this and handle when db has gone away.
            return result

    #I havnt checked this yet
    def delete(self, table, where=False):
        deleteStr = "delete from " + table
        deleteTuple = []
        if where:
            deleteStr += " where "
            first = True
            for key in where:
                if first:
                    first = False
                else:
                    deleteStr += " and "

                deleteStr += key + "=" + self.getConnParam()
                deleteTuple.append(where[key])

        self.query(deleteStr)  # , deleteTuple

    #I havnt checked this yet
    def deleteTable(self, table):
        deleteStr = "DROP TABLE " + table
        self.query(deleteStr)

    def select(self, table, join=False, orderBy=False, groupBy=False, where=False, limit=False, what=False, between=False):
        selectStr = "select "
        if what:
            selectStr += what
        else:
            selectStr += "*"
        selectStr += " from " + table
        if join:
            first = True
            for key in list(join.keys()):
                if first:
                    first = False
                else:
                    pass
                    #selectStr += " and "
                selectStr += " left join "
                selectStr += key + " on " + join[key] + " "
        selectTuple = []

        # TODO: make sure key is not bad
        if where:
            selectStr += " where "
            first = True
            for key in list(where.keys()):
                if first:
                    first = False
                else:
                    selectStr += " and "
                if where[key] == "is null" or where[key] == "is not null":
                    selectStr += key + " '" + where[key] + "' "
                else:
                    selectStr += key
                    if key.find("=") == -1 and key.find(">") == -1 and key.find("<") == -1:
                        #print where[key]
                        selectStr += "='" + where[key] + "'"
                    else:
                        selectStr += "'" + where[key] + "'"
                    selectTuple.append(where[key])

        if between:
            selectStr = " BETWEEN " + str(between[0]) + " AND " + str(between[1])

        if groupBy:
            selectStr += " group by " + groupBy

        if orderBy:
            selectStr += " order by "
            first = True
            for key in list(orderBy.keys()):
                if first:
                    selectStr += key + " "
                    first = False
                else:
                    selectStr += ", " + key
                if orderBy[key] is not "none":
                    selectStr += orderBy[key]

        if limit:
            selectStr += " limit " + str(limit)
        return self.query(selectStr)  # , selectTuple

    def selectDistinct(self, table, join=False, orderBy=False, groupBy=False, where=False, limit=False, what=False, between=False):
        selectStr = "select "
        if what:
            selectStr += "distinct( "
            selectStr += what
            selectStr += " ) "
        else:
            self.logger.log("what field is required.", "ERROR")
            return
        selectStr += " from " + table
        if join:
            first = True
            for key in list(join.keys()):
                if first:
                    first = False
                else:
                    pass
                    #selectStr += " and "
                selectStr += " left join "
                selectStr += key + " on " + join[key] + " "
        selectTuple = []

        # TODO: make sure key is not bad
        if where:
            selectStr += " where "
            first = True
            for key in list(where.keys()):
                if first:
                    first = False
                else:
                    selectStr += " and "
                if where[key] == "is null" or where[key] == "is not null":
                    selectStr += key + " '" + where[key] + "' "
                else:
                    selectStr += key
                    if key.find("=") == -1 and key.find(">") == -1 and key.find("<") == -1:
                        #print where[key]
                        selectStr += "='" + where[key] + "'"
                    else:
                        selectStr += "'" + where[key] + "'"
                    selectTuple.append(where[key])

        if between:
            selectStr = " BETWEEN " + str(between[0]) + " AND " + str(between[1])

        if groupBy:
            selectStr += " group by " + groupBy

        if orderBy:
            selectStr += " order by "
            first = True
            for key in list(orderBy.keys()):
                if first:
                    selectStr += key + " "
                    first = False
                else:
                    selectStr += ", " + key
                if orderBy[key] is not "none":
                    selectStr += orderBy[key]

        if limit:
            selectStr += " limit " + str(limit)

        return self.query(selectStr)  # , selectTuple

    def insert(self, table, data):
        insertStr = "insert into " + table + " ("
        insertTuple = []

        first = True
        for key in list(data.keys()):
            if first:
                first = False
            else:
                insertStr += ", "
            insertStr += key

        insertStr += ") values ('"

        first = True
        for i in list(data.keys()):
            if first:
                first = False
                insertStr += data[i]
            else:
                insertStr += "', '" + data[i]
            insertTuple.append(data[i])

        insertStr += "')"
        query = self.query(insertStr)
        insertID = str(self.query("SELECT LAST_INSERT_ID();")[0][0])
        if query == ():
            query = insertID
        else:
            query = query + insertID
        return query

    def update(self, table, data, where):
        updateStr = "update " + table + " set "
        updateTuple = []

        # TODO: make sure key is not bad
        first = True
        for key in list(data.keys()):
            if first:
                first = False
            else:
                updateStr += ", "
            updateStr += key + "='" + str(data[key]) + "'"
            updateTuple.append(data[key])

        updateStr += " where "

        first = True
        for key in list(where.keys()):
            if first:
                first = False
            else:
                updateStr += " and "
            if where[key] == "is null" or where[key] == "is not null":
                updateStr += key + " '" + where[key] + "'"
            else:
                updateStr += key + "='" + where[key] + "'"
                updateTuple.append(where[key])

        return self.query(updateStr)  # , updateTuple

    # Return true on insert, false on update
    def insertOrUpdate(self, table, data, on={}):
        if not on:
            # If on is empty insert if data is not find
            result = self.select(table, where=data)
            if not result:
                self.insert(table, data)
                return True
        else:
            # Select by on.  If found and different, update.
            # If found and the same do nothing
            # If not found insert.
            result = self.select(table, where=on)
            # TODO: handle update
            if not result:
                self.insert(table, data)
                return True
            else:
                self.update(table, data, on)
        return False

    def inTransaction(self):
        return self.transactionDepth > 0

    def beginTransaction(self):
        self.transactionDepth += 1
        if self.transactionDepth == 1:
            self.getConn().begin()
        #if self.transactionDepth == 1:
        #    print "DB begin transaction"

    def rollbackTransaction(self):
        self.transactionDepth = 0
        try:
            self.getConn().rollback()
        except Exception as e:
            if self.logger is not None:
                self.logger.log(e, 'WARNING')
            else:
                print((e))
        #print "DB rollback transaction"

    def commitTransaction(self):
        if self.transactionDepth == 1:
            self.transactionDepth = 0
            self.getConn().commit()
        if self.transactionDepth >= 1:
            self.transactionDepth -= 1
            #if self.transactionDepth == 0:
            #    print "DB committed transaction"
            #else:
            #    print "DB reduce transaction depth"
