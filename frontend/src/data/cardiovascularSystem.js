export const cardiovascularSystem = {
  system_id: 'sys_cardiovascular', system_name: 'Sistem Kardiovaskular', version: '1.0.0',
  model_3d_source: '/assets/models/3d/cardiovascular_system.glb',
  organs: [{
    organ_id: 'organ_heart', organ_name: 'Jantung (Cor)', mesh_node_name: 'Node_Heart_Mesh_3D',
    camera_focus_position: { x: 0, y: 1.2, z: 0.5 },
    sub_structures: [{ structure_id: 'struct_left_ventricle', name: 'Ventriculus Sinistrum (Bilik Kiri)', mesh_node_name: 'Mesh_Left_Ventricle', description: 'Memompa darah kaya O2 ke seluruh tubuh melalui aorta.' }],
    biochemical_parameters: {
      biomarkers: [
        { code: 'CK-MB', name: 'Creatine Kinase-MB', normal_range: '0 – 5 ng/mL', unit: 'ng/mL', chemsphere_compound_id: 'cmp_ckmb_enzyme' },
        { code: 'cTnT', name: 'Cardiac Troponin T', normal_range: '0 – 0.014 ng/mL', unit: 'ng/mL', chemsphere_compound_id: 'cmp_troponin_t' },
      ], metabolic_pathways: ['Beta-oksidasi asam lemak', 'Glikolisis & produksi ATP'],
    },
    pharmacology_receptors: [{ receptor_name: 'Reseptor adrenergik Beta-1', target_drug_class: 'Beta-blocker (mis. bisoprolol, atenolol)', chemsphere_reaction_id: 'rxn_beta1_inhibition' }],
  }],
  pathology_scenarios: [{
    scenario_id: 'scen_myocardial_infarction', disease_code_icd10: 'I21.9', disease_name: 'Infark Miokard Akut (Serangan Jantung)',
    affected_mesh_nodes: ['Mesh_Coronary_Artery_LAD', 'Mesh_Heart_Apex'],
    visual_effects: { mesh_color_tint: '#3a1d1d', pulse_rate_bpm: 110, arrhythmia_pattern: 'ST-Elevation' },
    biochemical_alterations: [{ biomarker_code: 'cTnT', simulated_value: 0.85 }, { biomarker_code: 'CK-MB', simulated_value: 24.5 }],
  }],
}
