"use client";
import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";

// Use environment variable for API URL, fallback to localhost for local dev
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:5020";

type MultiAgentResponse = {
  answer: string;
  context: Array<{
    score: number;
    payload: {
      key?: string;
      title?: string;
      description?: string;
      [key: string]: unknown;
    };
  }>;
  metadata: {
    agent_used: string;
    processing_time: number;
    query_type: string;
    user_flags: {
      user_can_wait: boolean;
      production_incident: boolean;
    };
  };
};

const SAMPLE_QUESTIONS = `# Sample Questions for Cuttlefish3

This document provides sample questions that users can ask the Cuttlefish3 system, organized by use case categories. These questions are based on the actual JIRA data patterns and the use cases identified in the Cuttlefish3.md analysis.

## Technical Troubleshooting Questions

### Memory and Performance Issues
- "How do I fix OutOfMemoryError: GC overhead limit exceeded in Eclipse?"
- "What causes memory leaks when scanning multiple XML documents?"
- "How to resolve performance issues with BeanUtils.copyProperties()?"
- "What are common causes of OutOfMemoryError in JBoss Tools?"
- "How do I fix memory issues with XStream marshalling?"

### Framework-Specific Issues

#### Spring Framework
- "How do I fix ClassCastException issues with SAXParserFactory?"
- "What causes 'XStream marshalling ended with exception' errors?"
- "How to resolve ServletTestExecutionListener breaking old code?"
- "What causes BeanFactory.getBeanNamesForAnnotation() issues?"
- "How do I fix GenericTypeAwarePropertyDescriptor problems?"
- "What causes XStreamMarshaller converterRegistry field to be null?"
- "How to resolve EhCacheFactoryBean race conditions?"
- "What causes ControllerAdvice annotation not being found?"

#### HBase Issues
- "How do I fix Region Server connection issues?"
- "What causes HBase Master recovery failures?"
- "How to resolve HBase table creation errors?"
- "What causes 'Region is being opened' exceptions?"
- "How do I fix HBase compaction failures?"
- "What causes HBase split transaction errors?"

#### JBoss/Eclipse Issues
- "How do I fix JBoss Tools installation errors?"
- "What causes Eclipse OSGi framework errors?"
- "How to resolve JBoss Central dependency issues?"
- "What causes OpenShift deployment URL problems?"
- "How do I fix JBoss Tools archetype lookup issues?"

#### RichFaces Issues
- "How do I fix JavaScript errors in RichFaces orderingList?"
- "What causes mobile responsiveness issues in RichFaces?"
- "How to resolve RichFaces picklist rendering problems?"
- "What causes RichFaces showcase mobile display issues?"

### Configuration and Setup Issues
- "How do I configure Spring context component scanning?"
- "What causes Maven dependency resolution failures?"
- "How to resolve Eclipse plugin compatibility issues?"
- "What causes OpenShift application deployment failures?"
- "How do I fix Java EE project archetype issues?"

## Bug Pattern Recognition Questions

### Common Error Patterns
- "What are the most common causes of OutOfMemoryError in Eclipse?"
- "How do I identify and fix XStream marshalling issues?"
- "What patterns indicate HBase region server problems?"
- "How to recognize and resolve Spring BeanFactory issues?"
- "What are common indicators of JBoss Tools installation problems?"

### Framework Migration Issues
- "What breaks when migrating from Spring 3.2.5 to 4.0.0?"
- "How do I identify compatibility issues when upgrading JBoss Tools?"
- "What causes problems when upgrading HBase versions?"
- "How to resolve Eclipse plugin version conflicts?"

## Project-Specific Questions

### Priority-Based Queries
- "What are the most critical issues in JBoss Tools?"
- "How do I find all Blocker priority issues in Spring Framework?"
- "What Major issues exist in HBase project?"
- "How to identify Critical issues across all projects?"

### Project Distribution
- "What issues exist in the JBIDE project?"
- "How do I find Spring Framework (SPR) related problems?"
- "What HBase (HBASE) issues should I be aware of?"
- "How to identify RichFaces (RF) specific problems?"

## Development Environment Questions

### IDE and Tool Issues
- "How do I fix Eclipse memory allocation problems?"
- "What causes JBoss Tools startup failures?"
- "How to resolve Maven archetype dependency issues?"
- "What causes OpenShift deployment configuration problems?"

### Build and Deployment Issues
- "How do I fix Java EE project creation errors?"
- "What causes Maven repository configuration issues?"
- "How to resolve Eclipse plugin installation failures?"
- "What causes OpenShift application context path problems?"

## Specific Error Resolution Questions

### Stack Trace Analysis
- "How do I interpret 'java.lang.OutOfMemoryError: GC overhead limit exceeded'?"
- "What does 'XStream marshalling ended with exception' mean?"
- "How to understand 'Region is being opened' HBase errors?"
- "What causes 'BeanFactory.getBeanNamesForAnnotation()' failures?"

### Configuration Problems
- "How do I fix Spring context component scanning issues?"
- "What causes HBase table creation failures?"
- "How to resolve JBoss Tools archetype lookup problems?"
- "What causes RichFaces mobile responsiveness issues?"

## Framework-Specific Troubleshooting

### Spring Framework
- "How do I fix BeanUtils.copyProperties() issues?"
- "What causes XStreamMarshaller converter problems?"
- "How to resolve ServletTestExecutionListener conflicts?"
- "What causes GenericTypeAwarePropertyDescriptor errors?"

### HBase
- "How do I fix Region Server connection failures?"
- "What causes HBase Master recovery issues?"
- "How to resolve HBase compaction problems?"
- "What causes HBase split transaction failures?"

### JBoss Tools
- "How do I fix JBoss Tools installation on Fedora?"
- "What causes Eclipse OSGi framework errors?"
- "How to resolve JBoss Central dependency issues?"
- "What causes OpenShift deployment URL problems?"

### RichFaces
- "How do I fix JavaScript errors in RichFaces components?"
- "What causes mobile display issues in RichFaces?"
- "How to resolve RichFaces picklist rendering problems?"
- "What causes RichFaces showcase mobile issues?"

## Performance and Optimization Questions

### Memory Management
- "How do I optimize Eclipse memory usage?"
- "What causes memory leaks in XML processing?"
- "How to resolve HBase memory allocation issues?"
- "What causes Spring BeanFactory memory problems?"

### Performance Tuning
- "How do I improve HBase region server performance?"
- "What causes slow Spring application startup?"
- "How to optimize JBoss Tools loading times?"
- "What causes RichFaces component rendering delays?"

## Integration and Compatibility Questions

### Version Compatibility
- "What breaks when upgrading Spring Framework versions?"
- "How do I ensure JBoss Tools compatibility with Eclipse versions?"
- "What causes HBase version upgrade issues?"
- "How to resolve RichFaces version conflicts?"

### Platform-Specific Issues
- "How do I fix JBoss Tools on Linux distributions?"
- "What causes OpenShift deployment issues on different platforms?"
- "How to resolve Eclipse plugin compatibility across platforms?"
- "What causes mobile device compatibility issues?"

## Advanced Troubleshooting Questions

### Complex Error Scenarios
- "How do I debug multiple concurrent HBase region server failures?"
- "What causes cascading Spring BeanFactory initialization errors?"
- "How to resolve Eclipse plugin dependency resolution loops?"
- "What causes RichFaces component state management issues?"

### Root Cause Analysis
- "How do I identify the root cause of OutOfMemoryError patterns?"
- "What causes recurring XStream marshalling failures?"
- "How to trace HBase region server connection issues?"
- "What causes persistent JBoss Tools installation problems?"

## Best Practices and Prevention Questions

### Error Prevention
- "How do I prevent OutOfMemoryError in Eclipse?"
- "What are best practices for HBase configuration?"
- "How to avoid Spring BeanFactory initialization issues?"
- "What causes preventable RichFaces rendering problems?"

### Configuration Best Practices
- "How do I properly configure Spring context scanning?"
- "What are recommended HBase region server settings?"
- "How to configure JBoss Tools for optimal performance?"
- "What are best practices for RichFaces mobile development?"

## Project Management Questions

### Issue Tracking
- "How do I find all Critical priority issues across projects?"
- "What are the most common issue types in each project?"
- "How to identify recurring patterns in bug reports?"
- "What causes the highest number of duplicate issues?"

### Release Planning
- "What are the most critical issues blocking releases?"
- "How do I identify issues that affect multiple projects?"
- "What causes the most customer impact across projects?"
- "How to prioritize issues based on severity and frequency?"

## Production Incident Troubleshooting

### Release Ticket Analysis
- "Which PCR release tickets contain critical security vulnerabilities?"
- "What release tickets (PCR-*) caused production outages?"
- "Which release tickets included memory leak fixes?"
- "What release tickets contained performance regression fixes?"
- "Which PCR tickets addressed null pointer exceptions?"

### Critical Issue Identification
- "What Critical priority release tickets were deployed recently?"
- "Which release tickets contained 'thread safety' fixes?"
- "What PCR tickets addressed 'configuration error' issues?"
- "Which release tickets included 'validation error' fixes?"
- "What release tickets contained 'serialization problem' fixes?"

### Security and Vulnerability Tracking
- "Which PCR tickets addressed security vulnerabilities?"
- "What release tickets included security scan results?"
- "Which PCR tickets contained DisplayObject security fixes?"
- "What release tickets addressed EventDispatcher security issues?"
- "Which PCR tickets included Container module security patches?"

### Performance Incident Correlation
- "Which release tickets caused performance regressions?"
- "What PCR tickets included memory usage optimizations?"
- "Which release tickets contained 'performance improvement' fixes?"
- "What release tickets addressed 'resource cleanup' issues?"
- "Which PCR tickets included 'code optimization' changes?"

### Compatibility and Breaking Changes
- "Which release tickets caused API compatibility issues?"
- "What PCR tickets included 'breaking change' fixes?"
- "Which release tickets addressed cross-platform compatibility?"
- "What release tickets contained 'API compatibility' fixes?"
- "Which PCR tickets included 'compatibility maintained' notes?"

### Module-Specific Incident Analysis
- "Which PCR tickets addressed DisplayObject module issues?"
- "What release tickets contained Module module fixes?"
- "Which PCR tickets included Container module patches?"
- "What release tickets addressed DataBinding module issues?"
- "Which PCR tickets contained UIComponent module fixes?"

### Release Timeline Correlation
- "What release tickets were deployed before the incident?"
- "Which PCR tickets were released in the last 30 days?"
- "What release tickets contained fixes for the affected modules?"
- "Which PCR tickets addressed similar issues in the past?"
- "What release tickets included the specific error patterns?"

### Hotfix and Emergency Release Identification
- "Which PCR tickets were marked as Critical priority?"
- "What release tickets contained emergency fixes?"
- "Which PCR tickets were released outside normal schedule?"
- "What release tickets included 'urgent' or 'hotfix' in description?"
- "Which PCR tickets addressed production-blocking issues?"

### Bug Fix Correlation
- "Which PCR tickets contained the specific bug fix (FLEX-XXXXX)?"
- "What release tickets included fixes for null pointer exceptions?"
- "Which PCR tickets addressed configuration error fixes?"
- "What release tickets contained validation error fixes?"
- "Which PCR tickets included thread safety improvements?"

### Release Impact Assessment
- "What was the scope of changes in PCR-XXX release?"
- "Which modules were affected in the latest release?"
- "What fixes were included in the problematic release?"
- "Which PCR tickets had the highest number of bug fixes?"
- "What release tickets contained the most critical fixes?"

### Rollback and Recovery Analysis
- "Which PCR tickets can be safely rolled back?"
- "What release tickets included rollback instructions?"
- "Which PCR tickets contained breaking changes that can't be rolled back?"
- "What release tickets included compatibility notes?"
- "Which PCR tickets had the least impact for rollback?"`;

export default function Home() {
  const [activeTab, setActiveTab] = useState<"query" | "reference">("query");
  const [query, setQuery] = useState("");
  const [userCanWait, setUserCanWait] = useState(true);
  const [productionIncident, setProductionIncident] = useState(false);
  const [result, setResult] = useState<MultiAgentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const res = await fetch(`${API_URL}/multiagent-rag`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          query: query.trim(),
          user_can_wait: userCanWait,
          production_incident: productionIncident
        }),
      });
      
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || err.error || "Request failed");
      }
      
      const data = await res.json();
      setResult(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Request failed");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      handleSubmit();
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <img
            src="/Cuttlefish3.png"
            alt="Cuttlefish3 logo"
            className="mx-auto mb-6 object-contain drop-shadow-md"
            style={{ width: '504px', height: '168px' }}
          />
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Cuttlefish3
          </h1>
          <p className="text-xl text-gray-600">
            Multi-Agent RAG System for Intelligent JIRA Ticket Retrieval
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab("query")}
                className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                  activeTab === "query"
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                }`}
              >
                Query
              </button>
              <button
                onClick={() => setActiveTab("reference")}
                className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                  activeTab === "reference"
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                }`}
              >
                Reference Queries
              </button>
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="max-w-4xl mx-auto">
          {activeTab === "query" ? (
            <div className="bg-white rounded-xl shadow-lg p-8">
              {/* Toggle Switches */}
              <div className="mb-8 flex flex-wrap gap-6">
                <div className="flex items-center space-x-3">
                  <span className="text-sm font-medium text-gray-700">
                    Not Urgent
                  </span>
                  <label className="toggle">
                    <input
                      type="checkbox"
                      checked={userCanWait}
                      onChange={(e) => setUserCanWait(e.target.checked)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-sm font-medium text-gray-700">
                    Production Issue
                  </span>
                  <label className="toggle toggle-urgent">
                    <input
                      type="checkbox"
                      checked={productionIncident}
                      onChange={(e) => setProductionIncident(e.target.checked)}
                    />
                    <span className="slider"></span>
                  </label>
                </div>
              </div>

              {/* Query Input */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Query
                </label>
                <textarea
                  className="w-full border border-gray-300 rounded-lg px-4 py-3 min-h-[120px] focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 resize-vertical"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={handleKeyPress}
                  placeholder="Enter your JIRA ticket query here... (Cmd/Ctrl + Enter to submit)"
                  disabled={loading}
                />
                <p className="text-xs text-gray-500 mt-1">
                  Tip: Use Cmd+Enter (Mac) or Ctrl+Enter (Windows/Linux) to submit
                </p>
              </div>

              {/* Submit Button */}
              <button
                className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg px-6 py-3 font-semibold hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-md hover:shadow-lg"
                onClick={handleSubmit}
                disabled={loading || !query.trim()}
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Processing...
                  </div>
                ) : (
                  "Search JIRA Tickets"
                )}
              </button>

              {/* Error Display */}
              {error && (
                <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-red-800">Error</h3>
                      <div className="mt-1 text-sm text-red-700">{error}</div>
                    </div>
                  </div>
                </div>
              )}

              {/* Results Display */}
              {result && (
                <div className="mt-8 space-y-6">
                  {/* Answer Section */}
                  <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                    <h3 className="text-lg font-semibold text-green-800 mb-3">
                      Answer
                    </h3>
                    <div className="text-gray-800 whitespace-pre-line leading-relaxed">
                      {result.answer}
                    </div>
                  </div>

                  {/* Context/Tickets Section */}
                  {result.context && result.context.length > 0 && (
                    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                      <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                        <h3 className="text-lg font-semibold text-gray-800">
                          Related JIRA Tickets ({result.context.length})
                        </h3>
                      </div>
                      <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                          <thead className="bg-gray-50">
                            <tr>
                              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Key
                              </th>
                              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Title
                              </th>
                            </tr>
                          </thead>
                          <tbody className="bg-white divide-y divide-gray-200">
                            {result.context.map((item, idx) => (
                              <tr key={idx} className="hover:bg-gray-50 transition-colors duration-150">
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
                                  {item.payload?.key || "N/A"}
                                </td>
                                <td className="px-6 py-4 text-sm text-gray-900">
                                  {item.payload?.title || "N/A"}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}

                  {/* Metadata Section */}
                  {result.metadata && (
                    <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                      <h3 className="text-lg font-semibold text-gray-800 mb-4">
                        Query Metadata
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="font-medium text-gray-600">Agent Used:</span>
                          <span className="ml-2 text-gray-800">{result.metadata.agent_used}</span>
                        </div>
                        <div>
                          <span className="font-medium text-gray-600">Processing Time:</span>
                          <span className="ml-2 text-gray-800">{result.metadata.processing_time?.toFixed(2)}s</span>
                        </div>
                        <div>
                          <span className="font-medium text-gray-600">Query Type:</span>
                          <span className="ml-2 text-gray-800">{result.metadata.query_type}</span>
                        </div>
                        <div>
                          <span className="font-medium text-gray-600">User Flags:</span>
                          <div className="ml-2 text-gray-800">
                            <div>Not Urgent: {result.metadata.user_flags?.user_can_wait ? "Yes" : "No"}</div>
                            <div>Production Issue: {result.metadata.user_flags?.production_incident ? "Yes" : "No"}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-8 py-6">
                <h2 className="text-2xl font-bold text-white">Reference Queries</h2>
                <p className="text-blue-100 mt-1">Sample questions organized by category to help you get started</p>
              </div>
              <div className="p-8">
                <div className="prose prose-lg max-w-none prose-headings:text-gray-800 prose-h1:text-3xl prose-h1:font-bold prose-h1:mb-6 prose-h1:pb-3 prose-h1:border-b prose-h1:border-gray-200 prose-h2:text-2xl prose-h2:font-semibold prose-h2:mt-8 prose-h2:mb-4 prose-h2:text-blue-800 prose-h3:text-xl prose-h3:font-medium prose-h3:mt-6 prose-h3:mb-3 prose-h3:text-blue-700 prose-h4:text-lg prose-h4:font-medium prose-h4:mt-4 prose-h4:mb-2 prose-h4:text-blue-600 prose-p:text-gray-700 prose-p:leading-relaxed prose-ul:space-y-1 prose-li:text-gray-700 prose-strong:text-gray-800 prose-code:bg-gray-100 prose-code:px-1 prose-code:py-0.5 prose-code:rounded prose-code:text-sm prose-code:font-mono">
                  <ReactMarkdown
                    components={{
                      h1: ({ children }) => (
                        <h1 className="text-3xl font-bold mb-6 pb-3 border-b border-gray-200 text-gray-800">
                          {children}
                        </h1>
                      ),
                      h2: ({ children }) => (
                        <h2 className="text-2xl font-semibold mt-8 mb-4 text-blue-800 border-l-4 border-blue-500 pl-4">
                          {children}
                        </h2>
                      ),
                      h3: ({ children }) => (
                        <h3 className="text-xl font-medium mt-6 mb-3 text-blue-700">
                          {children}
                        </h3>
                      ),
                      h4: ({ children }) => (
                        <h4 className="text-lg font-medium mt-4 mb-2 text-blue-600">
                          {children}
                        </h4>
                      ),
                      ul: ({ children }) => (
                        <ul className="space-y-2 ml-4">
                          {children}
                        </ul>
                      ),
                      li: ({ children }) => (
                        <li className="text-gray-700 flex items-start">
                          <span className="text-blue-500 mr-2 mt-1.5 flex-shrink-0">•</span>
                          <span className="hover:text-blue-800 transition-colors cursor-pointer">
                            {children}
                          </span>
                        </li>
                      ),
                      p: ({ children }) => (
                        <p className="text-gray-700 leading-relaxed mb-4">
                          {children}
                        </p>
                      ),
                      code: ({ children }) => (
                        <code className="bg-gray-100 px-2 py-1 rounded text-sm font-mono text-gray-800">
                          {children}
                        </code>
                      ),
                    }}
                  >
                    {SAMPLE_QUESTIONS}
                  </ReactMarkdown>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}