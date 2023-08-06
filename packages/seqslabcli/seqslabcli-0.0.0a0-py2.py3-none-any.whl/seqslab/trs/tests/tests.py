import json
import string
import random
from seqslab.tests.util import TestShell
from seqslab.trs.commands import BaseTools
from unittest import TestCase, main
from unittest.mock import patch
from os.path import dirname, abspath, join
from tenacity import retry, wait_fixed, stop_after_attempt
from seqslab.trs.register.azure import AzureTRSregister
from seqslab.trs.resource.azure import AzureResource
from functools import lru_cache


@retry(stop=stop_after_attempt(3), wait=wait_fixed(5), reraise=True)
@lru_cache(maxsize=16)
def mock_parameter(primary_descriptor: str, zip_file: str):
    return {
        "graph": "digraph igap {\n  #rankdir=LR;\n  compound=true;\n\n  # Links\n  CALL_preprocess -> CALL_iter_mapping\n  CALL_assembly -> CALL_rp\n  CALL_iter_mapping -> CALL_rp\n  CALL_preprocess -> CALL_assembly\n\n  # Nodes\n  CALL_iter_mapping [label=\"call iter_mapping\";shape=\"oval\";peripheries=2]\n  CALL_rp [label=\"call rp\";shape=\"oval\";peripheries=2]\n  CALL_assembly [label=\"call assembly\";shape=\"oval\";peripheries=2]\n  CALL_preprocess [label=\"call preprocess\";shape=\"oval\";peripheries=2]\n}",
        "subgraphs": [
            "digraph assembly {\n  #rankdir=LR;\n  compound=true;\n\n  # Links\n  CALL_assemble -> CALL_normalize\n  CALL_minimap2 -> CALL_normalize\n  CALL_assemble -> CALL_minimap2\n\n  # Nodes\n  CALL_normalize [label=\"call normalize\"]\n  CALL_assemble [label=\"call assemble\"]\n  CALL_minimap2 [label=\"call minimap2\"]\n}\n",
            "digraph report {\n  #rankdir=LR;\n  compound=true;\n\n  # Links\n  \n\n  # Nodes\n  CALL_gen_report [label=\"call gen_report\"]\n}\n",
            "digraph iter_mapping {\n  #rankdir=LR;\n  compound=true;\n\n  # Links\n  CALL_init -> CALL_iter_2\n\n  # Nodes\n  CALL_iter_2 [label=\"call iter_2\";shape=\"oval\";peripheries=2]\n  CALL_init [label=\"call init\";shape=\"oval\";peripheries=2]\n}\n",
            "digraph run_iter {\n  #rankdir=LR;\n  compound=true;\n\n  # Links\n  CALL_pileup_n_frq -> CALL_var_scan\n  CALL_pileup_n_frq -> CALL_gen_new_ref\n  CALL_sort_bam -> CALL_pileup_n_frq\n  CALL_mapping -> CALL_sort_bam\n\n  # Nodes\n  CALL_pileup_n_frq [label=\"call pileup_n_frq\"]\n  CALL_sort_bam [label=\"call sort_bam\"]\n  CALL_gen_new_ref [label=\"call gen_new_ref\"]\n  CALL_var_scan [label=\"call var_scan\"]\n  CALL_mapping [label=\"call mapping\"]\n}\n",
            "digraph preprocess {\n  #rankdir=LR;\n  compound=true;\n\n  # Links\n  CALL_combine_unpaired -> CALL_hisat2\n  CALL_trimmomatic -> CALL_hisat2\n  CALL_trimmomatic -> CALL_combine_unpaired\n\n  # Nodes\n  CALL_trimmomatic [label=\"call trimmomatic\"]\n  CALL_hisat2 [label=\"call hisat2\"]\n  CALL_combine_unpaired [label=\"call combine_unpaired\"]\n}\n"
        ],
        "inputs": {
            "igap.len": "Int (optional, default = 36)",
            "igap.read_group": "String",
            "igap.virus_ref": "File",
            "igap.ref": "File",
            "igap.fq_name": "String",
            "igap.input_fq": "Array[File]",
            "igap.ref_basename": "String",
            "igap.coverage": "Int (optional, default = 200)",
            "igap.platform_type": "String",
            "igap.iter_num": "Int (optional, default = 2)",
            "igap.freq": "Float (optional, default = 0.25)"
        },
        "configs": {
            "igap.assembly.assemble.paired_mapped_1_fq": "opp_generic-singular_auto",
            "igap.assembly.assemble.paired_mapped_2_fq": "opp_generic-singular_auto",
            "igap.assembly.assemble.unpaired_mapped_fq": "opp_generic-singular_auto",
            "igap.assembly.minimap2.fasta": "opp_generic-singular_auto",
            "igap.assembly.minimap2.ref": "opp_generic-singular_auto",
            "igap.assembly.normalize.fasta": "opp_generic-singular_auto",
            "igap.assembly.normalize.relative_strand": "opp_generic-singular_auto",
            "igap.iter_mapping.init.gen_new_ref.fqy": "opp_generic-singular_auto",
            "igap.iter_mapping.init.gen_new_ref.ref_fas": "opp_generic-singular_auto",
            "igap.iter_mapping.init.mapping.forward_fq": "opp_generic-singular_auto",
            "igap.iter_mapping.init.mapping.ref_fas": "opp_generic-singular_auto",
            "igap.iter_mapping.init.mapping.reverse_fq": "opp_generic-singular_auto",
            "igap.iter_mapping.init.mapping.single_fq": "opp_generic-singular_auto",
            "igap.iter_mapping.init.pileup_n_frq.ref_fas": "opp_generic-singular_auto",
            "igap.iter_mapping.init.pileup_n_frq.sorted_bam": "opp_generic-singular_auto",
            "igap.iter_mapping.init.sort_bam.bam": "opp_generic-singular_auto",
            "igap.iter_mapping.init.var_scan.pileup": "opp_generic-singular_auto",
            "igap.iter_mapping.iter_2.gen_new_ref.fqy": "opp_generic-singular_auto",
            "igap.iter_mapping.iter_2.gen_new_ref.ref_fas": "opp_generic-singular_auto",
            "igap.iter_mapping.iter_2.mapping.forward_fq": "opp_generic-singular_auto",
            "igap.iter_mapping.iter_2.mapping.ref_fas": "opp_generic-singular_auto",
            "igap.iter_mapping.iter_2.mapping.reverse_fq": "opp_generic-singular_auto",
            "igap.iter_mapping.iter_2.mapping.single_fq": "opp_generic-singular_auto",
            "igap.iter_mapping.iter_2.pileup_n_frq.ref_fas": "opp_generic-singular_auto",
            "igap.iter_mapping.iter_2.pileup_n_frq.sorted_bam": "opp_generic-singular_auto",
            "igap.iter_mapping.iter_2.sort_bam.bam": "opp_generic-singular_auto",
            "igap.iter_mapping.iter_2.var_scan.pileup": "opp_generic-singular_auto",
            "igap.preprocess.combine_unpaired.forward_unpaired_fq": "opp_generic-singular_auto",
            "igap.preprocess.combine_unpaired.reverse_unpaired_fq": "opp_generic-singular_auto",
            "igap.preprocess.hisat2.forward_fq": "opp_generic-singular_auto",
            "igap.preprocess.hisat2.ref": "opp_generic-singular_auto",
            "igap.preprocess.hisat2.reverse_fq": "opp_generic-singular_auto",
            "igap.preprocess.hisat2.single_fq": "opp_generic-singular_auto",
            "igap.preprocess.trimmomatic.r1_fq": "opp_generic-singular_auto",
            "igap.preprocess.trimmomatic.r2_fq": "opp_generic-singular_auto",
            "igap.rp.gen_report.bam": "opp_generic-singular_auto",
            "igap.rp.gen_report.new_ref": "opp_generic-singular_auto",
            "igap.rp.gen_report.normalized_fa": "opp_generic-singular_auto",
            "igap.rp.gen_report.virus_ref": "opp_generic-singular_auto"
        },
        "runtime_options": [
            {
                "name": "acu-m4",
                "description": "Memory optimized 4-core cluster compute (Runtime 2.0, Spark 3.3, Python 3.8, Java 1.8.0, Cromwell 63)",
                "settings": {
                    "type": "batch.core.windows.net",
                    "vm_size": "Standard_D12_v2",
                    "workers": {
                        "spot": 0,
                        "dedicated": 1
                    },
                    "auto_scale": False,
                    "worker_on_master": True
                },
                "options": [
                    "spark.driver.cores 1",
                    "spark.driver.memory 536870912",
                    "spark.executor.cores 1",
                    "spark.executor.memory 7g",
                    "spark.dynamicAllocation.enabled true",
                    "spark.shuffle.service.enabled true",
                    "spark.dynamicAllocation.minExecutors 1",
                    "spark.kryo.registrator org.bdgenomics.adam.serialization.ADAMKryoRegistrator",
                    "spark.local.dir /mnt"
                ]
            },
            {
                "name": "acu-m8",
                "description": "Memory optimized 8-core cluster compute (Runtime 2.0, Spark 3.3, Python 3.8, Java 1.8.0, Cromwell 63)",
                "settings": {
                    "type": "batch.core.windows.net",
                    "vm_size": "Standard_D13_v2",
                    "workers": {
                        "spot": 0,
                        "dedicated": 1
                    },
                    "auto_scale": False,
                    "worker_on_master": True
                },
                "options": [
                    "spark.driver.cores 1",
                    "spark.driver.memory 536870912",
                    "spark.executor.cores 1",
                    "spark.executor.memory 7g",
                    "spark.dynamicAllocation.enabled true",
                    "spark.shuffle.service.enabled true",
                    "spark.dynamicAllocation.minExecutors 1",
                    "spark.kryo.registrator org.bdgenomics.adam.serialization.ADAMKryoRegistrator",
                    "spark.local.dir /mnt"
                ]
            },
            {
                "name": "acu-m16s",
                "description": "Memory optimized 16-core spot cluster compute (Runtime 2.0, Spark 3.3, Python 3.8, Java 1.8.0, Cromwell 63)",
                "settings": {
                    "type": "batch.core.windows.net",
                    "vm_size": "Standard_D13_v2",
                    "workers": {
                        "spot": 1,
                        "dedicated": 1
                    },
                    "auto_scale": False,
                    "worker_on_master": True
                },
                "options": [
                    "spark.driver.cores 1",
                    "spark.driver.memory 1g",
                    "spark.executor.cores 1",
                    "spark.executor.memory 7g",
                    "spark.dynamicAllocation.enabled true",
                    "spark.shuffle.service.enabled true",
                    "spark.dynamicAllocation.minExecutors 1",
                    "spark.kryo.registrator org.bdgenomics.adam.serialization.ADAMKryoRegistrator",
                    "spark.local.dir /mnt"
                ]
            },
            {
                "name": "acu-m64",
                "description": "Memory optimized 64-core cluster compute (Runtime 2.0, Spark 3.3, Python 3.8, Java 1.8.0, Cromwell 63)",
                "settings": {
                    "type": "batch.core.windows.net",
                    "vm_size": "Standard_D14_v2",
                    "workers": {
                        "spot": 0,
                        "dedicated": 4
                    },
                    "auto_scale": False,
                    "worker_on_master": True
                },
                "options": [
                    "spark.driver.cores 1",
                    "spark.driver.memory 1g",
                    "spark.executor.cores 1",
                    "spark.executor.memory 7g",
                    "spark.dynamicAllocation.enabled true",
                    "spark.shuffle.service.enabled true",
                    "spark.dynamicAllocation.minExecutors 1",
                    "spark.kryo.registrator org.bdgenomics.adam.serialization.ADAMKryoRegistrator",
                    "spark.local.dir /mnt"
                ]
            },
            {
                "name": "acu-m64s",
                "description": "Memory optimized 64-core spot cluster compute (Runtime 2.0, Spark 3.3, Python 3.8, Java 1.8.0, Cromwell 63)",
                "settings": {
                    "type": "batch.core.windows.net",
                    "vm_size": "Standard_D13_v2",
                    "workers": {
                        "spot": 3,
                        "dedicated": 5
                    },
                    "auto_scale": False,
                    "worker_on_master": True
                },
                "options": [
                    "spark.driver.cores 1",
                    "spark.driver.memory 1g",
                    "spark.executor.cores 1",
                    "spark.executor.memory 7g",
                    "spark.dynamicAllocation.enabled true",
                    "spark.shuffle.service.enabled true",
                    "spark.dynamicAllocation.minExecutors 1",
                    "spark.kryo.registrator org.bdgenomics.adam.serialization.ADAMKryoRegistrator",
                    "spark.local.dir /mnt"
                ]
            },
            {
                "name": "acu-m160s",
                "description": "Memory optimized 160-core spot cluster compute (Runtime 2.0, Spark 3.3, Python 3.8, Java 1.8.0, Cromwell 63)",
                "settings": {
                    "type": "batch.core.windows.net",
                    "vm_size": "Standard_D14_v2",
                    "workers": {
                        "spot": 4,
                        "dedicated": 6
                    },
                    "auto_scale": False,
                    "worker_on_master": True
                },
                "options": [
                    "spark.driver.cores 1",
                    "spark.driver.memory 536870912",
                    "spark.executor.cores 1",
                    "spark.executor.memory 7g",
                    "spark.dynamicAllocation.enabled true",
                    "spark.shuffle.service.enabled true",
                    "spark.dynamicAllocation.minExecutors 1",
                    "spark.kryo.registrator org.bdgenomics.adam.serialization.ADAMKryoRegistrator",
                    "spark.local.dir /mnt"
                ]
            }
        ],
        "operator_pipelines": [
            {
                "id": "opp_bam_auto-path",
                "description": "File-based BAM/SAM workload pipeline with no data parallelization.",
                "file_type": "bam,sam",
                "workload_type": "FILE",
                "operators": {
                    "format": {
                        "class": "com.atgenomix.seqslab.piper.operators.format.PartitionedFormat"
                    },
                    "p_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.pipe.PPipe"
                    }
                },
                "pipelines": {
                    "call": [
                        "format",
                        "p_pipe"
                    ]
                },
                "version": "2022-03-07",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_bam_partition-hg19-chromosomes",
                "description": "File-based BAM workload parallelization pipeline with each HG19 chromosome per partition.",
                "file_type": "bam",
                "workload_type": "FILE",
                "operators": {
                    "sink": {
                        "class": "com.atgenomix.seqslab.piper.operators.sink.HadoopSink"
                    },
                    "format": {
                        "class": "org.bdgenomics.adam.cli.piper.BamFormat"
                    },
                    "p_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.pipe.PPipe"
                    },
                    "source": {
                        "class": "org.bdgenomics.adam.cli.piper.BamSource"
                    },
                    "collect": {
                        "class": "com.atgenomix.seqslab.piper.operators.collect.LocalCollect"
                    },
                    "partition": {
                        "ref": "wasbs://static@seqslabbundles.blob.core.windows.net/reference/19/HG/ref.dict",
                        "class": "org.bdgenomics.adam.cli.piper.BamPartition",
                        "parallelism": "wasbs://static@seqslabbundles.blob.core.windows.net/system/bed/19/chromosomes"
                    }
                },
                "pipelines": {
                    "call": [
                        "format",
                        "p_pipe"
                    ],
                    "input": [
                        "source",
                        "partition",
                        "format"
                    ],
                    "output": [
                        "collect",
                        "sink"
                    ]
                },
                "version": "2022-03-07",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_fastq_auto-path",
                "description": "File-based Fastq workload pipeline with no data parallelization.",
                "file_type": "fastq,fastq.gz,fq.gz",
                "workload_type": "FILE",
                "operators": {
                    "sink": {
                        "class": "com.atgenomix.seqslab.piper.operators.sink.HadoopSink"
                    },
                    "format": {
                        "class": "com.atgenomix.seqslab.piper.operators.format.PartitionedFormat"
                    },
                    "p_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.pipe.PPipe"
                    },
                    "collect": {
                        "class": "com.atgenomix.seqslab.piper.operators.collect.LocalCollect"
                    }
                },
                "pipelines": {
                    "call": [
                        "format",
                        "p_pipe"
                    ],
                    "output": [
                        "collect",
                        "sink"
                    ]
                },
                "version": "2022-03-07",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_fastq_partition-145728_path",
                "description": "File-based Fastq workload parallelization pipeline with 145728 read records each partition.",
                "file_type": "fastq,fastq.gz,fq.gz",
                "workload_type": "FILE",
                "operators": {
                    "sink": {
                        "class": "com.atgenomix.seqslab.piper.operators.sink.HadoopSink"
                    },
                    "format": {
                        "class": "com.atgenomix.seqslab.piper.operators.format.FastqFormat"
                    },
                    "p_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.pipe.PPipe"
                    },
                    "source": {
                        "class": "com.atgenomix.seqslab.piper.operators.source.FastqSource",
                        "codec": "org.seqdoop.hadoop_bam.util.BGZFEnhancedGzipCodec"
                    },
                    "collect": {
                        "class": "com.atgenomix.seqslab.piper.operators.collect.LocalCollect"
                    },
                    "partition": {
                        "class": "com.atgenomix.seqslab.piper.operators.partition.FastqPartition",
                        "parallelism": "145728"
                    }
                },
                "pipelines": {
                    "call": [
                        "format",
                        "p_pipe"
                    ],
                    "input": [
                        "source",
                        "partition",
                        "format"
                    ],
                    "output": [
                        "collect",
                        "sink"
                    ]
                },
                "version": "2022-03-07",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_fastq_partition-145728_stdin",
                "description": "File-based Fastq workload parallelization pipeline with 145728 read records each partition via stdin.",
                "file_type": "fastq,fastq.gz,fq.gz",
                "workload_type": "FILE",
                "operators": {
                    "format": {
                        "class": "com.atgenomix.seqslab.piper..operators.format.FastqFormat"
                    },
                    "p_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.pipe.PPipe"
                    },
                    "source": {
                        "class": "com.atgenomix.seqslab.piper.operators.source.FastqSource",
                        "codec": "org.seqdoop.hadoop_bam.util.BGZFEnhancedGzipCodec"
                    },
                    "partition": {
                        "class": "com.atgenomix.seqslab.piper.operators.partition.FastqPartition",
                        "parallelism": "145728"
                    }
                },
                "pipelines": {
                    "call": [
                        "format",
                        "c_pipe"
                    ],
                    "input": [
                        "source",
                        "partition",
                        "format"
                    ]
                },
                "version": "2022-03-07",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_file_auto",
                "description": "File-based workload pipeline with intrinsic data parallelization.",
                "file_type": "*",
                "workload_type": "FILE",
                "operators": {
                    "sink": {
                        "class": "com.atgenomix.seqslab.piper.operators.sink.HadoopSink"
                    },
                    "c_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.pipe.CPipe"
                    },
                    "source": {
                        "class": "com.atgenomix.seqslab.piper.operators.source.PartitionedSource"
                    },
                    "collect": {
                        "class": "com.atgenomix.seqslab.piper.operators.collect.LocalCollect"
                    }
                },
                "pipelines": {
                    "call": [
                        "source",
                        "p_pipe"
                    ],
                    "output": [
                        "collect",
                        "sink"
                    ]
                },
                "version": "2022-03-07",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_file_auto_stdin",
                "description": "File-based workload pipeline with intrinsic data parallelization via stdin.",
                "file_type": "*",
                "workload_type": "FILE",
                "operators": {
                    "sink": {
                        "class": "com.atgenomix.seqslab.piper.operators.sink.HadoopSink"
                    },
                    "c_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.pipe.CPipe"
                    },
                    "source": {
                        "class": "com.atgenomix.seqslab.piper.operators.source.PartitionedSource"
                    },
                    "collect": {
                        "class": "com.atgenomix.seqslab.piper.operators.collect.LocalCollect"
                    }
                },
                "pipelines": {
                    "call": [
                        "source",
                        "c_pipe"
                    ],
                    "output": [
                        "collect",
                        "sink"
                    ]
                },
                "version": "2022-03-07",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_generic-single-file_auto",
                "description": "Automatic workload pipeline for both regular files, e.g. genome reference and dataset of one single file.",
                "file_type": "*",
                "workload_type": "REGULAR",
                "operators": {
                    "format": {
                        "class": "com.atgenomix.seqslab.piper.operators.SingleFileFormat"
                    },
                    "p_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.PPipe"
                    }
                },
                "pipelines": {
                    "call": [
                        "format",
                        "p_pipe"
                    ]
                },
                "version": "2021-12-01",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_generic-singular_auto",
                "description": "Automatic single-partitioned workload pipeline for input files, e.g. genome reference file hg19.fa, input dirs containing multiple files or subdirectories, e.g. genome reference directory, and intermediate datasets of one single file.",
                "file_type": "*",
                "workload_type": "DEFAULT",
                "operators": {
                    "format": {
                        "class": "com.atgenomix.seqslab.piper.operators.format.SingularFormat"
                    },
                    "p_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.pipe.PPipe"
                    }
                },
                "pipelines": {
                    "call": [
                        "format",
                        "p_pipe"
                    ]
                },
                "version": "2022-03-07",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_memory_auto",
                "description": "Memory-based workload pipeline with intrinsic data parallelization.",
                "file_type": "*",
                "workload_type": "MEMORY",
                "operators": {
                    "sink": {
                        "class": "com.atgenomix.seqslab.piper.operators.sink.HadoopSink"
                    },
                    "m_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.pipe.MPipe"
                    },
                    "source": {
                        "class": "com.atgenomix.seqslab.piper.operators.source.PartitionedSource"
                    },
                    "collect": {
                        "class": "com.atgenomix.seqslab.piper.operators.collect.LocalCollect"
                    }
                },
                "pipelines": {
                    "call": [
                        "source",
                        "m_pipe"
                    ],
                    "output": [
                        "collect",
                        "sink"
                    ]
                },
                "version": "2021-07-18",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_regular-dir_auto",
                "description": "Automatic workload pipeline for regular directories that contain multiple files or subdirectories and can be shared across cluster environment.",
                "file_type": "*",
                "workload_type": "REGULAR",
                "operators": {
                    "format": {
                        "class": "com.atgenomix.seqslab.piper.operators.RegularDir"
                    },
                    "p_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.PPipe"
                    }
                },
                "pipelines": {
                    "call": [
                        "format",
                        "p_pipe"
                    ]
                },
                "version": "2021-07-18",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_regular-file_auto",
                "description": "Automatic workload pipeline for regular files, e.g. genome reference, that can be shared across cluster environment.",
                "file_type": "*",
                "workload_type": "REGULAR",
                "operators": {
                    "format": {
                        "class": "com.atgenomix.seqslab.piper.operators.RegularFile"
                    },
                    "p_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.PPipe"
                    }
                },
                "pipelines": {
                    "call": [
                        "format",
                        "p_pipe"
                    ]
                },
                "version": "2021-07-18",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_shared-dir_auto",
                "description": "Automatic workload pipeline for shared directories that contain multiple files or subdirectories and can be shared across cluster environment.",
                "file_type": "*",
                "workload_type": "SHARED",
                "operators": {
                    "format": {
                        "class": "com.atgenomix.seqslab.piper.operators.format.SharedDir"
                    },
                    "p_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.pipe.PPipe"
                    }
                },
                "pipelines": {
                    "call": [
                        "format",
                        "p_pipe"
                    ]
                },
                "version": "2022-03-07",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_shared-file_auto",
                "description": "Automatic workload pipeline for shared files, e.g. genome reference, that can be shared across cluster environment.",
                "file_type": "*",
                "workload_type": "SHARED",
                "operators": {
                    "format": {
                        "class": "com.atgenomix.seqslab.piper.operators.format.SharedFile"
                    },
                    "p_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.pipe.PPipe"
                    }
                },
                "pipelines": {
                    "call": [
                        "format",
                        "p_pipe"
                    ]
                },
                "version": "2022-03-07",
                "cus_id": "cus_InryDNsBjHKDq8n"
            },
            {
                "id": "opp_vcf_partition-hg19-chromosomes",
                "description": "File-based VCF workload parallelization pipeline with each HG19 chromosome per partition.",
                "file_type": "vcf,gvcf,vcf.gz,gvcf.gz",
                "workload_type": "FILE",
                "operators": {
                    "sink": {
                        "class": "com.atgenomix.seqslab.piper.operators.sink.HadoopSink"
                    },
                    "format": {
                        "class": "com.atgenomix.seqslab.piper.operators.format.VcfFormat"
                    },
                    "p_pipe": {
                        "class": "com.atgenomix.seqslab.piper.operators.pipe.PPipe"
                    },
                    "source": {
                        "class": "com.atgenomix.seqslab.piper.operators.source.VcfSource"
                    },
                    "collect": {
                        "class": "com.atgenomix.seqslab.piper.operators.collect.LocalCollect"
                    },
                    "partition": {
                        "ref": "wasbs://static@seqslabbundles.blob.core.windows.net/reference/19/HG/ref.dict",
                        "class": "com.atgenomix.seqslab.piper.operators.partition.VcfPartition",
                        "parallelism": "wasbs://static@seqslabbundles.blob.core.windows.net/system/bed/19/chromosomes"
                    }
                },
                "pipelines": {
                    "call": [
                        "format",
                        "p_pipe"
                    ],
                    "input": [
                        "source",
                        "partition",
                        "format"
                    ],
                    "output": [
                        "collect",
                        "sink"
                    ]
                },
                "version": "2022-03-07",
                "cus_id": "cus_InryDNsBjHKDq8n"
            }
        ],
        "workflows": [
            {
                "name": "assembly.wdl",
                "path": "wdl/assembly.wdl",
                "file_type": "SECONDARY_DESCRIPTOR",
                "workflow_name": "assembly",
                "image_name": ""
            },
            {
                "name": "report.wdl",
                "path": "wdl/report.wdl",
                "file_type": "SECONDARY_DESCRIPTOR",
                "workflow_name": "report",
                "image_name": ""
            },
            {
                "name": "iter-mapping.wdl",
                "path": "wdl/iter-mapping.wdl",
                "file_type": "SECONDARY_DESCRIPTOR",
                "workflow_name": "iter_mapping",
                "image_name": ""
            },
            {
                "name": "main.wdl",
                "path": "wdl/main.wdl",
                "file_type": "PRIMARY_DESCRIPTOR",
                "workflow_name": "igap",
                "image_name": ""
            },
            {
                "name": "run-iter.wdl",
                "path": "wdl/run-iter.wdl",
                "file_type": "SECONDARY_DESCRIPTOR",
                "workflow_name": "run_iter",
                "image_name": ""
            },
            {
                "name": "preprocess.wdl",
                "path": "wdl/preprocess.wdl",
                "file_type": "SECONDARY_DESCRIPTOR",
                "workflow_name": "preprocess",
                "image_name": ""
            }
        ],
        "calls": {
            "wdl/main.wdl": {
                "preprocess": [
                    "preprocess"
                ],
                "iter": [
                    "iter"
                ],
                "assembly": [
                    "assembly"
                ],
                "report": [
                    "rp"
                ]
            },
            "wdl/assembly.wdl": {
                "assemble": [
                    "assemble"
                ],
                "minimap2": [
                    "minimap2"
                ],
                "normalize": [
                    "normalize"
                ]
            },
            "wdl/preprocess.wdl": {
                "trimmomatic": [
                    "trimmomatic"
                ],
                "combine": [
                    "combine"
                ],
                "hisat2": [
                    "hisat2"
                ]
            },
            "wdl/report.wdl": {
                "gen": [
                    "gen"
                ]
            },
            "wdl/iter-mapping.wdl": {
                "run": [
                    "run",
                    "run"
                ]
            },
            "wdl/run-iter.wdl": {
                "mapping": [
                    "mapping"
                ],
                "sort": [
                    "sort"
                ],
                "pileup": [
                    "pileup"
                ],
                "gen": [
                    "gen"
                ],
                "var": [
                    "var"
                ]
            }
        }
    }


class mock_Resource(AzureResource):
    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5), reraise=True)
    @lru_cache(maxsize=16)
    def container_registry(name) -> dict:
        return {
            "id": "/subscriptions/62fccd52-f6fe-4f3b-aa3a-bfe2b4ae0bbc/resourceGroups/atgxtestws/providers/Microsoft"
                  ".ContainerRegistry/registries/atgxtestws62fccacr",
            "name": "atgxtestws62fccacr",
            "location": "westus2",
            "login_server": "atgxtestws62fccacr.azurecr.io",
            "admin_user": True,
            "authorization": "Basic YXRneHRlc3R3czYyZmNjYWNyOnFoMm9vU1R2Uz0wQmt6RVZiakhYbEF2ZFR0MWwzZDZn",
            "repositories": [
                {
                    "name": "atgenomix/seqslab_runtime-1.4_ubuntu-18.04_gatk4",
                    "tags": [
                        {
                            "name": "2022-01-22-07-00",
                            "digest": "sha256:493a88037f22ff1f4454d8977fa95225460fbd4c823e7ad2e65a168b0af854cb",
                            "created": "2022-01-22T07:33:05.6010297Z",
                            "last_updated": "2022-01-22T07:33:05.6010297Z",
                            "size": 3082465110,
                            "type": "docker"
                        },
                        {
                            "name": "2022-01-22-09-45",
                            "digest": "sha256:694fd6c44b792708922403d10b86a44f429f905cc97276fb334afe004b1fb3df",
                            "created": "2022-01-22T11:44:49.7140945Z",
                            "last_updated": "2022-01-22T11:44:49.7140945Z",
                            "size": 3088748536,
                            "type": "docker"
                        },
                        {
                            "name": "2022-01-09-02-00",
                            "digest": "sha256:8117fa6678d846bd11620eb9daeefe85037a5afe4ad920cf552fcbc7c478c6c8",
                            "created": "2022-01-12T03:30:41.0375026Z",
                            "last_updated": "2022-01-12T03:30:41.0375026Z",
                            "size": 3072366309,
                            "type": "docker"
                        },
                        {
                            "name": "2022-01-18-04-14",
                            "digest": "sha256:b4f8c266658b3d3a1e43785b4dc7f4f29e95caa35679d41efb226472660eeb8f",
                            "created": "2022-01-22T01:45:45.0746722Z",
                            "last_updated": "2022-01-22T01:45:45.0746722Z",
                            "size": 3072453965,
                            "type": "docker"
                        },
                        {
                            "name": "2021-12-29-07-28",
                            "digest": "sha256:f6dafa531c4814bc013d5929d93578a2e12ad053f9283c5f1ab78d935395a8fa",
                            "created": "2021-12-29T12:23:55.7253318Z",
                            "last_updated": "2021-12-29T12:23:55.7253318Z",
                            "size": 3071923050,
                            "type": "docker"
                        }
                    ]
                },
                {
                    "name": "atgenomix/seqslab_runtime-1.4_ubuntu-18.04_hicpro",
                    "tags": [
                        {
                            "name": "2021-12-29-07-28",
                            "digest": "sha256:220febcaf664946aaed00fc22007d840416617dd81dc6ac3de736eccdf3d171f",
                            "created": "2021-12-29T08:26:32.5508052Z",
                            "last_updated": "2021-12-29T08:26:32.5508052Z",
                            "size": 3062954586,
                            "type": "docker"
                        },
                        {
                            "name": "2022-01-17-07-36",
                            "digest": "sha256:30e38c21b119266f42ca316b64222f319f7d01d38de48e77d3516080b4c006b2",
                            "created": "2022-01-17T08:01:22.2105367Z",
                            "last_updated": "2022-01-17T08:01:22.2105367Z",
                            "size": 3063710321,
                            "type": "docker"
                        },
                        {
                            "name": "2021-12-17-10-24",
                            "digest": "sha256:39a3ea9fafe8ada7985f1ec80674ad17252b321216a79371dbbfb256397aabfa",
                            "created": "2021-12-17T02:33:59.3956584Z",
                            "last_updated": "2021-12-17T02:33:59.3956584Z",
                            "size": 3029167678,
                            "type": "docker"
                        },
                        {
                            "name": "2022-01-18-04-14",
                            "digest": "sha256:7f53d204fa0bf986edc7a5c2564273f6aa986623239dff92e3670845f23a5e99",
                            "created": "2022-01-26T05:20:26.6844863Z",
                            "last_updated": "2022-01-26T05:20:26.6844863Z",
                            "size": 3062198892,
                            "type": "docker"
                        },
                        {
                            "name": "2022-01-09-02-00",
                            "digest": "sha256:90c6102c57a028127af33f42f7fda17e057badfc1655207fb7bd0cf20709c210",
                            "created": "2022-01-12T03:32:18.5785938Z",
                            "last_updated": "2022-01-12T03:32:18.5785938Z",
                            "size": 3063522956,
                            "type": "docker"
                        }
                    ]
                },
                {
                    "name": "atgenomix/seqslab_runtime-1.4_ubuntu-18.04_iter_mapping",
                    "tags": [
                        {
                            "name": "2022-01-21-11-50",
                            "digest": "sha256:4d066951e4c6551b656f91237a6867309ad11f26b52c860c721bc0a7004a232d",
                            "created": "2022-01-21T08:55:01.0940729Z",
                            "last_updated": "2022-01-21T08:55:01.0940729Z",
                            "size": 2437559017,
                            "type": "docker"
                        }
                    ]
                },
                {
                    "name": "samples/nginx",
                    "tags": [
                        {
                            "name": "latest",
                            "digest": "sha256:57a94fc99816c6aa225678b738ac40d85422e75dbb96115f1bb9b6ed77176166",
                            "created": "2021-08-10T09:52:49.1368541Z",
                            "last_updated": "2021-08-10T09:52:49.1368541Z",
                            "size": 7737579,
                            "type": "docker"
                        }
                    ]
                }
            ]
        }

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5), reraise=True)
    @lru_cache(maxsize=16)
    def workspace(name) -> list:
        return [
            {
                "id": "/subscriptions/62fccd52-f6fe-4f3b-aa3a-bfe2b4ae0bbc/resourceGroups/atgxtestws/providers"
                      "/Microsoft.Batch/batchAccounts/atgxtestws62fccbatch",
                "name": "atgxtestws62fccbatch",
                "type": "Microsoft.Batch/batchAccounts",
                "location": "westus2",
                "identity": {
                    "type": "None"
                }
            },
            {
                "id": "/subscriptions/62fccd52-f6fe-4f3b-aa3a-bfe2b4ae0bbc/resourceGroups/atgxtestws/providers"
                      "/Microsoft.ContainerRegistry/registries/atgxtestws62fccacr",
                "name": "atgxtestws62fccacr",
                "type": "Microsoft.ContainerRegistry/registries",
                "sku": {
                    "name": "Basic",
                    "tier": "Basic"
                },
                "location": "westus2",
                "tags": {}
            },
            {
                "id": "/subscriptions/62fccd52-f6fe-4f3b-aa3a-bfe2b4ae0bbc/resourceGroups/atgxtestws/providers"
                      "/Microsoft.Network/virtualNetworks/atgxtestws62fccbatch-vnet",
                "name": "atgxtestws62fccbatch-vnet",
                "type": "Microsoft.Network/virtualNetworks",
                "location": "westus2"
            },
            {
                "id": "/subscriptions/62fccd52-f6fe-4f3b-aa3a-bfe2b4ae0bbc/resourceGroups/atgxtestws/providers"
                      "/Microsoft.Storage/storageAccounts/atgxtestws62fccstorage",
                "name": "atgxtestws62fccstorage",
                "type": "Microsoft.Storage/storageAccounts",
                "sku": {
                    "name": "Standard_LRS",
                    "tier": "Standard"
                },
                "kind": "StorageV2",
                "location": "westus2",
                "tags": {
                    "atgenomix.workspace": "bio.seqslab.azure.drs",
                    "ms-resource-usage": "azure-cloud-shell"
                }
            }
        ]


class mock_TRSregister(AzureTRSregister):

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
    def post_tool(data: dict) -> dict:
        return {
            "id": f"{data.get('id')}",
            "toolclass": {
                "name": "string",
                "description": "string"
            },
            "name": "string",
            "description": "string",
            "aliases": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
            },
            "has_checker": True,
            "checker_url": "string"
        }

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
    def post_version(data: dict, tool_id: str, workspace: str) -> dict:
        return {
            "images": [
                {
                    "checksum": {
                        "checksum": "57a94fc99816c6aa225678b738ac40d85422e75dbb96115f1bb9b6ed77176166",
                        "type": "sha256"
                    },
                    "image_type": "Docker",
                    "image_name": "samples/nginx",
                    "registry_host": "seqslabapi97e51acr.azurecr.io",
                    "size": 7737579,
                    "updated_time": "2022-02-22T07:23:10.836205Z"
                },
                {
                    "checksum": {
                        "checksum": "57a94fc99816c6aa225678b738ac40d85422e75dbb96115f1bb9b6ed77176157",
                        "type": "sha256"
                    },
                    "image_type": "Docker",
                    "image_name": "samples/nginx4",
                    "registry_host": "seqslabapi97e51acr.azurecr.io",
                    "size": 773757121214214,
                    "updated_time": "2022-02-22T07:23:10.849083Z"
                }
            ],
            "access_url": "https://atgxtestws62fccstorage.dfs.core.windows.net/seqslab/trs/trs_test_NqIlrIzNKp/1.0",
            "descriptor_type": [
                "WDL"
            ],
            "author": [],
            "name": None,
            "version_id": "1.0",
            "is_production": False,
            "meta_version": "2022-02-22T07:23:10.820474Z",
            "verified": False,
            "verified_source": [],
            "signed": False,
            "included_apps": [],
            "url": "/trs/v2/tools/trs_test_NqIlrIzNKp/versions/1.0/"
        }

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
    def post_file(data: dict, zip_file: str, tool_id: str, version_id: str,
                  descriptor_type: str) -> str:
        return mock_TRSregister.TRS_TOOLFILE_URL.format(tool_id=tool_id,
                                                        version_id=version_id,
                                                        descriptor_type=descriptor_type)

    @staticmethod
    def get_tool():
        return {
            'results': [{
                "id": "trs_iYv6vasXL7mu7Cu",
                "name": "Seqslab-Hail",
                "description": "Leverage Hail on Seqslab V3 Platform",
                "meta_version": "2021-12-14T03:01:37.852139Z",
                "aliases": {},
                "organization": "cus_Hy8DlcOkaSItHwm",
                "toolclass": {
                    "id": 3,
                    "name": "InteractiveNotebook",
                    "description": "InteractiveNotebook"
                },
                "has_checker": True,
                "checker_url": "https://github.com/hail-is/hail",
                "versions": [
                    {
                        "images": [
                            {
                                "checksum": {
                                    "checksum": "56656d521a88764cba1e3965a1bbba8699f91544017efe59af26703b18605da8",
                                    "type": "sha256"
                                },
                                "image_type": "Docker",
                                "image_name": "atgenomix/seqslab_runtime-1.3_ubuntu-18.04_hail-annotation:latest",
                                "registry_host": "atgenomix.azurecr.io",
                                "size": 0,
                                "updated_time": "2021-12-14T03:01:39.062798Z"
                            }
                        ],
                        "access_url": "https://atgxtestws62fccstorage.dfs.core.windows.net/seqslab/trs"
                                      "/trs_iYv6vasXL7mu7Cu/1.0",
                        "descriptor_type": [
                            "JNB"
                        ],
                        "author": {},
                        "name": "Seqslab-Hail",
                        "version_id": "1.0",
                        "is_production": True,
                        "meta_version": "2021-12-14T03:01:39.042726Z",
                        "verified": True,
                        "verified_source": {},
                        "signed": True,
                        "included_apps": {},
                        "url": "http://dev-api.seqslab.net/trs/v2/tools/trs_iYv6vasXL7mu7Cu/versions/1.0/"
                    }
                ],
                "url": "http://dev-api.seqslab.net/trs/v2/tools/trs_iYv6vasXL7mu7Cu/"
            }]}

    @staticmethod
    def delete_version(tid: str, vid: str):
        return f"Delete completely."

    @staticmethod
    def get_file(tool_id: str, version_id: str, download_path: str, descriptor_type: str):
        return 200


class mock_Tools(BaseTools):
    """Mock register commands"""

    def __init__(self):
        pass


class CommandSpecTest(TestCase):
    def setUp(self) -> None:
        self.trs_id = "trs_test_4QLix7cSvY"
        self.trs_version = "1.0"
        self.descriptor_type = "WDL"
        self.workspace = "atgxtestws"
        self.working_dir = f'{dirname(abspath(__file__))}/working-dir/'

    @staticmethod
    def _make_name():
        return "test_tool" + ''.join(random.choices(
            string.ascii_letters + string.digits, k=5)
        )

    @patch('seqslab.trs.register.azure.AzureTRSregister', mock_TRSregister)
    def test_command_trs_tool(self):
        tool = mock_Tools()
        tool_name = self._make_name()
        shell = TestShell(commands=[tool.tool])
        value = shell.run_cli_line(
            f"test_shell tool --name {tool_name} --id {self.trs_id}")
        self.assertEqual(0, value)

    @patch('seqslab.trs.register.azure.AzureTRSregister', mock_TRSregister)
    def test_command_trs_version(self):
        tool = mock_Tools()
        version_name = self._make_name()
        images = [{"registry_host": "seqslabapi97e51acr.azurecr.io",
                   "image_name": "samples/nginx", "size": 7737579,
                   "checksum": "sha256:57a94fc99816c6aa225678b738ac40d85422e75dbb96115f1bb9b6ed77176166",
                   "image_type": "Docker"},
                  {"registry_host": "seqslabapi97e51acr.azurecr.io", "image_name": "samples/nginx4",
                   "size": 773757121214214,
                   "checksum": "sha256:57a94fc99816c6aa225678b738ac40d85422e75dbb96115f1bb9b6ed77176157",
                   "image_type": "Docker"}]
        shell = TestShell(commands=[tool.version])
        value = shell.run_cli_line(
            f"test_shell version --workspace {self.workspace} --name {version_name} --tool-id {self.trs_id} "
            f'--descriptor-type {self.descriptor_type} --id {self.trs_version} '
            f'--images {json.dumps(images).replace(" ", "")}')
        self.assertEqual(0, value)

    @patch('seqslab.trs.register.azure.AzureTRSregister', mock_TRSregister)
    def test_command_trs_file(self):
        tool = mock_Tools()
        shell = TestShell(commands=[tool.file])
        value = shell.run_cli_line(
            f"test_shell file --tool-id {self.trs_id} --version-id {self.trs_version} "
            f"--descriptor-type {self.descriptor_type} --working-dir {self.working_dir} "
            f"--file-info execs/exec-template.json")
        self.assertEqual(0, value)

    @patch('seqslab.trs.resource.azure.AzureResource', mock_Resource)
    def test_command_trs_images(self):
        tool = mock_Tools()
        shell = TestShell(commands=[tool.images])
        value = shell.run_cli_line(
            f"test_shell images --workspace {self.workspace}")
        self.assertEqual(0, value)

    @patch('seqslab.wes.commands.Jobs.parameter', mock_parameter)
    @patch('seqslab.trs.resource.azure.AzureResource', mock_Resource)
    def test_command_trs_execs(self):
        tool = mock_Tools()
        shell = TestShell(commands=[tool.execs])
        value = shell.run_cli_line(
            f"test_shell execs --working-dir {self.working_dir} --main-wdl wdl/main.wdl "
            f"--inputs inputs.json --output execs/execs.json")
        self.assertEqual(0, value)

    @patch('seqslab.trs.register.azure.AzureTRSregister', mock_TRSregister)
    def test_command_trs_list(self):
        tool = mock_Tools()
        shell = TestShell(commands=[tool.list])
        value = shell.run_cli_line(
            f"test_shell list")
        self.assertEqual(0, value)

    @patch('seqslab.trs.register.azure.AzureTRSregister', mock_TRSregister)
    def test_command_trs_delete_version(self):
        tool = mock_Tools()
        shell = TestShell(commands=[tool.delete_version])
        value = shell.run_cli_line(
            f"test_shell delete-version --tool-id {self.trs_id} --version-id {self.trs_version}")
        self.assertEqual(0, value)

    @patch('seqslab.trs.register.azure.AzureTRSregister', mock_TRSregister)
    def test_command_trs_get(self):
        tool = mock_Tools()
        shell = TestShell(commands=[tool.get])
        value = shell.run_cli_line(
            f"test_shell get --tool-id {self.trs_id} --version-id {self.trs_version} "
            f"--descriptor-type {self.descriptor_type} --download-path {join(self.working_dir, 'download.zip')}")
        self.assertEqual(0, value)


if __name__ == "__main__":
    # main()
    test = CommandSpecTest()
    test.setUp()
    test.test_command_trs_execs()
