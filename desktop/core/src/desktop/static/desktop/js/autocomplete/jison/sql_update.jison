// Licensed to Cloudera, Inc. under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  Cloudera, Inc. licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

DataManipulation
 : UpdateStatement
 ;

DataManipulation_EDIT
 : UpdateStatement_EDIT
 ;

UpdateStatement
 : 'UPDATE' TargetTable 'SET' SetClauseList OptionalWhereClause
 ;

UpdateStatement_EDIT
 : 'UPDATE' TargetTable_EDIT 'SET' SetClauseList OptionalWhereClause
 | 'UPDATE' TargetTable 'SET' SetClauseList_EDIT OptionalWhereClause
 | 'UPDATE' TargetTable 'SET' SetClauseList OptionalWhereClause_EDIT
 | 'UPDATE' TargetTable 'SET' SetClauseList OptionalWhereClause 'CURSOR'
   {
     if (!$5) {
       suggestKeywords([ 'WHERE' ]);
     }
   }
 | 'UPDATE' TargetTable 'CURSOR'
   {
     suggestKeywords([ 'SET' ]);
   }
 | 'UPDATE' TargetTable_EDIT
 | 'UPDATE' TargetTable
 | 'UPDATE' 'CURSOR'
   {
     suggestTables();
     suggestDatabases({ appendDot: true });
   }
 ;

TargetTable
 : TableName
 ;

TargetTable_EDIT
 : TableName_EDIT
 ;

TableName
 : LocalOrSchemaQualifiedName
   {
     addTablePrimary($1);
   }
 ;

TableName_EDIT
 : LocalOrSchemaQualifiedName_EDIT
 ;

SetClauseList
 : SetClause
 | SetClauseList ',' SetClause
 ;

SetClauseList_EDIT
 : SetClause_EDIT
 | SetClauseList ',' SetClause_EDIT
 | SetClause_EDIT ',' SetClauseList
 | SetClauseList ',' SetClause_EDIT ',' SetClauseList
 ;

SetClause
 : SetTarget '=' UpdateSource
 ;

SetClause_EDIT
 : SetTarget '=' UpdateSource_EDIT
 | SetTarget 'CURSOR'
   {
     suggestKeywords([ '=' ]);
   }
 | 'CURSOR'
   {
     suggestColumns();
   }
 ;

SetTarget
 : ColumnReference
 ;

UpdateSource
 : ValueExpression
 ;

UpdateSource_EDIT
 : ValueExpression_EDIT
 ;