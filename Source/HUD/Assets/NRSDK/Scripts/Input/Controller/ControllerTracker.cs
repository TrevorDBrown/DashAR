/****************************************************************************
* Copyright 2019 Xreal Techonology Limited. All rights reserved.
*                                                                                                                                                          
* This file is part of NRSDK.                                                                                                          
*                                                                                                                                                           
* https://www.xreal.com/        
* 
*****************************************************************************/

namespace NRKernal
{
    using System.Collections;
    using System.Collections.Generic;
    using UnityEngine;
    
    /// <summary> A controller tracker. </summary>
    public class ControllerTracker : MonoBehaviour
    {
        /// <summary> The default hand enum. </summary>
        public ControllerHandEnum defaultHandEnum;
        /// <summary> The raycaster. </summary>
        public NRPointerRaycaster raycaster;
        /// <summary> The model anchor. </summary>
        public Transform modelAnchor;

        public bool recenterPitch = true;
        /// <summary> True if is enabled, false if not. </summary>
        private bool m_IsEnabled;
        /// <summary> True if is 6dof, false if not. </summary>
        private bool m_Is6dof;
        /// <summary> The default local offset. </summary>
        private Vector3 m_DefaultLocalOffset;
        /// <summary> Cache world matrix. </summary>
        private Matrix4x4 m_CachedWorldMatrix = Matrix4x4.identity;

        /// <summary> Gets the camera center. </summary>
        /// <value> The camera center. </value>
        private Transform CameraCenter
        {
            get
            {
                return NRInput.CameraCenter;
            }
        }

        private const float StillTime = 3.0f; //静止时间
        private float m_NoMovementTimer = 0; //没有移动计时器
        private float m_MovementThreshold = 0.3f; //度
        private Quaternion m_MovementRotation = Quaternion.identity;
        private bool m_Moveable = true;

        private float m_ReviseAngle = -7f;//双目时，需射线向上旋转 x 角度
        private Quaternion m_ReviseRotation = Quaternion.identity;
        
        private Quaternion controllerInverse = Quaternion.identity;
        private Quaternion rollRotation = Quaternion.identity;
        private Quaternion pitchRotation = Quaternion.identity;
        /// <summary> Awakes this object. </summary>
        private void Awake()
        {
            m_DefaultLocalOffset = transform.localPosition;
            raycaster.RelatedHand = defaultHandEnum;

            m_ReviseRotation = Quaternion.AngleAxis(m_ReviseAngle, Vector3.right);
        }

        /// <summary> Executes the 'enable' action. </summary>
        private void OnEnable()
        {
            NRInput.OnControllerRecentering += OnRecentering;
            NRInput.OnControllerStatesUpdated += OnControllerStatesUpdated;
            NRHMDPoseTracker.OnWorldPoseReset += OnWorldPoseReset;
        }

        /// <summary> Executes the 'disable' action. </summary>
        private void OnDisable()
        {
            NRInput.OnControllerRecentering -= OnRecentering;
            NRInput.OnControllerStatesUpdated -= OnControllerStatesUpdated;
            NRHMDPoseTracker.OnWorldPoseReset -= OnWorldPoseReset;
        }

        private void Start()
        {            
            m_Is6dof = NRInput.GetControllerAvailableFeature(ControllerAvailableFeature.CONTROLLER_AVAILABLE_FEATURE_POSITION)
                && NRInput.GetControllerAvailableFeature(ControllerAvailableFeature.CONTROLLER_AVAILABLE_FEATURE_ROTATION);
        }

        /// <summary> Executes the 'controller states updated' action. </summary>
        private void OnControllerStatesUpdated()
        {
            UpdateTracker();
        }

        /// <summary> Updates the tracker. </summary>
        private void UpdateTracker()
        {
            if (CameraCenter == null)
                return;
            m_IsEnabled = NRInput.CheckControllerAvailable(defaultHandEnum) && !NRInput.Hands.IsRunning;
            raycaster.gameObject.SetActive(m_IsEnabled && NRInput.RaycastersActive && NRInput.RaycastMode == RaycastModeEnum.Laser && m_Moveable);
            modelAnchor.gameObject.SetActive(m_IsEnabled);
            if (m_IsEnabled)
            {
                if(NRInput.RaycastersUpdatePose)
                    TrackPose();

                if (Quaternion.Angle(transform.rotation, m_MovementRotation) >= m_MovementThreshold || NRInput.GetButton(ControllerButton.TRIGGER))
                {
                    m_MovementRotation = transform.rotation;
                    m_Moveable = true;
                    m_NoMovementTimer = 0;
                }
                else
                {
                    if (m_Moveable)
                    {
                        m_NoMovementTimer += Time.deltaTime;
                        if (m_NoMovementTimer >= StillTime)
                        {
                            m_Moveable = false;
                        }
                    }
                    else if(Time.frameCount % 30 == 0)
                    {
                        m_MovementRotation = transform.rotation;
                    }
                }
            }
            
        }

        /// <summary> Track pose. </summary>
        private void TrackPose()
        {
            Pose poseInAPIWorld = new Pose(NRInput.GetPosition(defaultHandEnum), NRInput.GetRotation(defaultHandEnum));
            if (recenterPitch)
                poseInAPIWorld.rotation = poseInAPIWorld.rotation * controllerInverse;
            Pose pose = ApplyWorldMatrix(poseInAPIWorld);
            
            if (NRFrame.MonoMode)
            {
                transform.position = NRInput.CameraCenter.position;
                transform.rotation = pose.rotation * pitchRotation * rollRotation;
            }
            else
            {
                transform.position = m_Is6dof ? pose.position : CameraCenter.TransformPoint(m_DefaultLocalOffset);
                if (recenterPitch)
                    transform.rotation = pose.rotation * pitchRotation * m_ReviseRotation * rollRotation;
                else
                    transform.rotation = pose.rotation;
            }
        }

        /// <summary> Apply world transform. </summary>
        private Pose ApplyWorldMatrix(Pose pose)
        {
            var objectMatrix = ConversionUtility.GetTMatrix(pose.position, pose.rotation);
            var object_in_world = m_CachedWorldMatrix * objectMatrix;
            return new Pose(ConversionUtility.GetPositionFromTMatrix(object_in_world),
                ConversionUtility.GetRotationFromTMatrix(object_in_world));
        }

        
        /// <summary>
        ///     Recenter the φ coordinate of laser to make sure the laser is pointing to forward of camera. But the θ coordinate of the laser keeps in sync with controller device.
        /// </summary>
        private void OnRecentering(ControllerHandEnum handEnum)
        {
            if (gameObject.activeSelf && defaultHandEnum == handEnum)
            {
                StartCoroutine(SyncRecenter());
            }
        }

        private IEnumerator SyncRecenter()
        {
            yield return null;
            Plane horizontal_plane = new Plane(Vector3.up, Vector3.zero);
            Vector3 horizontalFoward = horizontal_plane.ClosestPointOnPlane(CameraCenter.forward).normalized;
            var horizontalRotEuler = Quaternion.LookRotation(horizontalFoward, Vector3.up).eulerAngles;

            // var worldMatrix = NRSessionManager.Instance.NRHMDPoseTracker.GetWorldOffsetMatrixFromNative();
            // var worldRot = ConversionUtility.GetRotationFromTMatrix(worldMatrix);
            // Quaternion correctRot = worldRot * Quaternion.Euler(0, horizontalRotEuler.y, 0);

            if (recenterPitch)
            {
                float offsetAngle  = Quaternion.LookRotation(CameraCenter.forward, Vector3.up).eulerAngles.x;
                pitchRotation      = Quaternion.AngleAxis(offsetAngle, Vector3.right);
                controllerInverse  = Quaternion.Inverse(NRInput.GetRotation(defaultHandEnum));

                float offsetZAngle = NRInput.GetRotation(defaultHandEnum).eulerAngles.z;
                rollRotation       = Quaternion.AngleAxis(offsetZAngle, Vector3.forward);
            }
            else
            {
                //m_ReviseRotation   = Quaternion.AngleAxis(m_ReviseAngle, Vector3.right);
                pitchRotation      = Quaternion.identity;
                rollRotation       = Quaternion.identity;
            }
                
            var verticalDegree = NRSessionManager.Instance.NRHMDPoseTracker.GetCachedWorldPitch();
            // Use the yaw of camera and the pitch of the world offset from native.
            Quaternion correctRot = Quaternion.Euler(verticalDegree, 0, 0) * Quaternion.Euler(0, horizontalRotEuler.y, 0);
            // For 6dof controller, the position should be cached as pose of controller device is reset.
            Vector3 position = m_Is6dof ? transform.position : Vector3.zero;
            m_CachedWorldMatrix = ConversionUtility.GetTMatrix(position, correctRot);
            NRDebugger.Info("[ControllerTracker] OnRecentering : forward={0}, horForw={1}, horRot={2}, vertRot={3}, correctRot={4}",
                CameraCenter.forward.ToString("F4"), horizontalFoward.ToString("F4"), horizontalRotEuler.ToString("F4"), verticalDegree.ToString("F4"), correctRot.eulerAngles.ToString("F4"));
        }

        private void OnWorldPoseReset()
        {
            NRInput.RecenterController();
        }
    }
}