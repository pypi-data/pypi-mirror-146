<?xml version='1.0'?> <!-- As XML file -->

<!--********************************************************************
Copyright 2022 Robert A. Beezer

This file is part of PreTeXt.

PreTeXt is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 or version 3 of the
License (at your option).

PreTeXt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PreTeXt.  If not, see <http://www.gnu.org/licenses/>.
*********************************************************************-->

<!-- http://pimpmyxslt.com/articles/entity-tricks-part2/ -->
<!DOCTYPE xsl:stylesheet [
    <!ENTITY % entities SYSTEM "entities.ent">
    %entities;
]>

<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:xml="http://www.w3.org/XML/1998/namespace"
>

<!-- Conversion of author source for Runestone/interactive exercises  -->
<!-- to "standard" PreTeXt exercises, which can be used as-is in      -->
<!-- *every* conversion, except the HTML conversion, where a more     -->
<!-- capable version is designed to be powered by Runestone Services. -->

<!-- We include text utilities so we can manipulate indentation -->
<!-- in blocks of code as part of Parsons problems              -->
<xsl:include href = "./pretext-text-utilities.xsl"/>

<!-- True/False -->

<xsl:template match="exercise[statement/@correct]" mode="runestone-to-static">
    <!-- prompt, followed by ordered list of choices -->
    <xsl:text>&#xa;</xsl:text>
    <statement>
        <xsl:copy-of select="statement/node()"/>
        <p>True or False?</p>
    </statement>
    <!-- Hints are authored, not derived from problem formulation -->
    <xsl:text>&#xa;</xsl:text>
    <xsl:copy-of select="hint"/>
    <!-- the answer, simply "True" or "False" -->
    <xsl:text>&#xa;</xsl:text>
    <answer>
        <xsl:choose>
            <xsl:when test="statement/@correct = 'yes'">
                <p>True.</p>
            </xsl:when>
            <xsl:when test="statement/@correct = 'no'">
                <p>False.</p>
            </xsl:when>
            <xsl:otherwise/>
        </xsl:choose>
    </answer>
    <!-- Answer, as above, plus explication with feedback -->
    <xsl:text>&#xa;</xsl:text>
    <solution>
        <xsl:choose>
            <xsl:when test="statement/@correct = 'yes'">
                <p>True.</p>
            </xsl:when>
            <xsl:when test="statement/@correct = 'no'">
                <p>False.</p>
            </xsl:when>
            <xsl:otherwise/>
        </xsl:choose>
        <xsl:copy-of select="feedback/node()"/>
    </solution>
</xsl:template>

<xsl:template match="exercise[statement and choices]" mode="runestone-to-static">
    <!-- prompt, followed by ordered list of choices -->
    <xsl:text>&#xa;</xsl:text>
    <statement>
        <xsl:copy-of select="statement/node()"/>
        <p><ol label="A."> <!-- conforms to RS markers -->
            <xsl:for-each select="choices/choice">
                <li>
                    <xsl:copy-of select="statement/node()"/>
                </li>
            </xsl:for-each>
        </ol></p>
    </statement>
    <!-- Hints are authored, not derived from problem formulation -->
    <xsl:text>&#xa;</xsl:text>
    <xsl:copy-of select="hint"/>
    <!-- the correct choices, as letters, in a sentence as a list -->
    <xsl:text>&#xa;</xsl:text>
    <answer>
        <p>
            <xsl:for-each select="choices/choice">
                <xsl:if test="@correct = 'yes'">
                    <xsl:number format="A"/>
                    <xsl:if test="following-sibling::choice[@correct = 'yes']">
                        <xsl:text>, </xsl:text>
                    </xsl:if>
                </xsl:if>
            </xsl:for-each>
            <xsl:text>.</xsl:text>
        </p>
    </answer>
    <!-- feedback for each choice, in a list -->
    <xsl:text>&#xa;</xsl:text>
    <solution>
        <p><ol label="A."> <!-- conforms to RS markers -->
            <xsl:for-each select="choices/choice">
                <li>
                    <title>
                        <xsl:choose>
                            <xsl:when test="@correct = 'yes'">
                                <xsl:text>Correct</xsl:text>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text>Incorrect</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </title>
                    <xsl:copy-of select="feedback/node()"/>
                </li>
            </xsl:for-each>
        </ol></p>
    </solution>
</xsl:template>

<xsl:template match="exercise[statement and blocks]" mode="runestone-to-static">
    <!-- determine these two options before context switches -->
    <xsl:variable name="b-natural" select="not(@language) or (@language = 'natural')"/>
    <xsl:variable name="b-indent" select="@indent = 'yes'"/>
    <statement>
        <xsl:copy-of select="statement/node()"/>
        <!-- blocks, in author-defined order, via @order attribute -->
        <p><ul>
            <xsl:for-each select="blocks/block">
                <xsl:sort select="@order"/>
                <li>
                    <xsl:choose>
                        <xsl:when test="choice">
                            <!-- a paired distractor in the block        -->
                            <!-- separate alternatives with "Either/Or"  -->
                            <!-- Order is as authored                    -->
                            <xsl:for-each select="choice">
                                <xsl:choose>
                                    <xsl:when test="following-sibling::choice">
                                        <p>Either:</p>
                                    </xsl:when>
                                    <xsl:when test="preceding-sibling::choice">
                                        <p>Or:</p>
                                    </xsl:when>
                                </xsl:choose>
                                <xsl:choose>
                                    <xsl:when test="$b-natural">
                                        <!-- replicate source of choice -->
                                        <xsl:copy-of select="node()"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <!-- computer code, make a code display           -->
                                        <!-- A "p" gets indentation relative to Either/Or -->
                                        <!-- Otherwsie, we could make a sublist?          -->
                                        <p>
                                            <cd>
                                                <xsl:choose>
                                                    <xsl:when test="$b-indent">
                                                        <xsl:apply-templates select="." mode="strip-cline-indentation"/>
                                                    </xsl:when>
                                                    <xsl:otherwise>
                                                        <xsl:copy-of select="node()"/>
                                                    </xsl:otherwise>
                                                </xsl:choose>
                                            </cd>
                                        </p>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:for-each>
                        </xsl:when>
                        <xsl:otherwise>
                            <!-- not a paired distractor -->
                            <xsl:choose>
                                <xsl:when test="$b-natural">
                                    <!-- replicate source of block -->
                                    <xsl:copy-of select="node()"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <!-- computer code, make a code display -->
                                    <cd>
                                        <xsl:choose>
                                            <xsl:when test="$b-indent">
                                                <!-- a hard problem, reader supplies indentation -->
                                                <xsl:apply-templates select="." mode="strip-cline-indentation"/>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <!-- a little help, indentation preserved and visible -->
                                                <xsl:attribute name="showspaces">
                                                    <xsl:text>all</xsl:text>
                                                </xsl:attribute>
                                                <xsl:text>&#xa;</xsl:text>
                                                <xsl:copy-of select="node()"/>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </cd>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:otherwise>
                    </xsl:choose>
                </li>
            </xsl:for-each>
        </ul></p>
    </statement>
    <solution>
        <xsl:choose>
            <xsl:when test="$b-natural">
                <!-- not a programming exercise, use unordered -->
                <!-- list and copy "natural" markup            -->
                <p><ul>
                    <xsl:for-each select="blocks/block">
                        <!-- default on "block" is  correct="yes" -->
                        <xsl:if test="not(@correct = 'no')">
                            <li>
                                <xsl:choose>
                                    <xsl:when test="choice">
                                        <!-- just the correct one -->
                                        <xsl:for-each select="choice">
                                            <xsl:if test="@correct = 'yes'">
                                                <xsl:copy-of select="node()"/>
                                            </xsl:if>
                                        </xsl:for-each>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:copy-of select="node()"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </li>
                        </xsl:if>
                    </xsl:for-each>
                </ul></p>
            </xsl:when>
            <xsl:otherwise>
                <!-- programming language specified, assume "cline" -->
                <!-- structure, reconstruct as a program/input      -->
                <program>
                    <xsl:attribute name="language">
                        <xsl:value-of select="@language"/>
                    </xsl:attribute>
                    <input>
                        <xsl:for-each select="blocks/block">
                            <xsl:if test="not(@correct = 'no')">
                                <xsl:choose>
                                    <xsl:when test="choice">
                                        <!-- just the correct choice              -->
                                        <!-- default on "choice" is  correct="no" -->
                                        <xsl:for-each select="choice">
                                            <xsl:if test="@correct = 'yes'">
                                                <xsl:for-each select="cline">
                                                    <xsl:value-of select="."/>
                                                    <xsl:text>&#xa;</xsl:text>
                                                </xsl:for-each>
                                            </xsl:if>
                                        </xsl:for-each>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:for-each select="cline">
                                            <xsl:value-of select="."/>
                                            <xsl:text>&#xa;</xsl:text>
                                        </xsl:for-each>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:if>
                        </xsl:for-each>
                    </input>
                </program>
            </xsl:otherwise>
        </xsl:choose>
    </solution>
</xsl:template>

<!-- If a sequence of "cline" are in a problem where a student does      -->
<!-- not get indentation help, then we need to strip it out for          -->
<!-- presentation in a static form.  This template forms the text block, -->
<!-- strips leading/gross indentation with a utility template, then uses -->
<!-- a recursive template to wrap back into "cline".                     -->

<xsl:template match="block|choice" mode="strip-cline-indentation">
    <xsl:variable name="text-block">
        <xsl:for-each select="cline">
            <xsl:value-of select="."/>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:variable>
    <xsl:call-template name="restore-cline">
        <xsl:with-param name="text">
            <xsl:call-template name="sanitize-text">
                <xsl:with-param name="text">
                    <xsl:value-of select="$text-block"/>
                </xsl:with-param>
            </xsl:call-template>
        </xsl:with-param>
    </xsl:call-template>
</xsl:template>

<xsl:template name="restore-cline">
    <xsl:param name="text"/>

    <xsl:choose>
        <xsl:when test="$text = ''"/>
        <xsl:otherwise>
            <cline>
                <xsl:value-of select="substring-before($text, '&#xa;')"/>
            </cline>
            <xsl:call-template name="restore-cline">
                <xsl:with-param name="text" select="substring-after($text, '&#xa;')"/>
            </xsl:call-template>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<!-- Active Code -->

<xsl:template match="exercise[statement and program]|project[statement and program]|activity[statement and program]|exploration[statement and program]|investigation[statement and program]" mode="runestone-to-static">
    <statement>
        <!-- duplicate the authored prompt/statement -->
        <xsl:copy-of select="statement/node()"/>
        <!-- bring up the program as part of the problem statement -->
        <xsl:copy-of select="program"/>
    </statement>
    <xsl:copy-of select="hint|answer|solution"/>
</xsl:template>

</xsl:stylesheet>
